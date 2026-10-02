"""Integration invariants for portable, read-only helper behavior."""

import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "reader-first"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = load("reader_first_checker", SKILL / "scripts" / "check.py")
context = load("reader_first_context", SKILL / "scripts" / "load_context.py")
installer = load("reader_first_installer", ROOT / "install.py")
packager = load("reader_first_packager", ROOT / "scripts" / "package.py")


def command(script, *args, stdin=None, cwd=None):
    return subprocess.run([sys.executable, "-B", str(script), *map(str, args)], input=stdin, capture_output=True, text=True, cwd=cwd)


class ScannerTests(unittest.TestCase):
    def test_locations_are_unicode_character_offsets_into_original(self):
        text = "é 🐘 heading\r\nA seamless experience.\nPivotal work."
        result = checker.scan(text, "sample")
        self.assertEqual([(x["line"], x["column"]) for x in result["candidates"]], [(2, 3), (3, 1)])
        for item in result["candidates"]:
            self.assertEqual(text[item["start"]:item["end"]], item["match"])

    def test_code_comments_and_destinations_are_masked_but_labels_remain(self):
        text = "\n".join([
            "```md", "seamless", "```", "~~~", "pivotal", "~~~", "    revolutionary",
            "`leverage` and ``best-in-class``.", "<!-- unparalleled -->",
            "[seamless](https://test.invalid/pivotal)", "https://test.invalid/revolutionary",
            "[link]: https://test.invalid/effortlessly", "After: pivotal.",
        ])
        result = checker.scan(text, "sample")
        self.assertEqual([x["match"] for x in result["candidates"]], ["seamless", "pivotal"])
        self.assertEqual([x["line"] for x in result["candidates"]], [10, 13])

    def test_unterminated_fence_and_comment_do_not_leak(self):
        self.assertEqual(checker.scan("```\nseamless", "sample")["candidates"], [])
        self.assertEqual(checker.scan("<!-- pivotal", "sample")["candidates"], [])

    def test_zero_candidates_does_not_assert_quality(self):
        result = checker.scan("Everything is ready.", "sample")
        self.assertEqual(result["candidates"], [])
        self.assertTrue(result["summary"]["contextual_review_required"])

    def test_developer_precision_is_a_candidate_not_an_auto_edit(self):
        text = "PostgreSQL logical replication with at-least-once delivery."
        result = checker.scan(text, "sample")
        self.assertEqual(text, "PostgreSQL logical replication with at-least-once delivery.")
        self.assertTrue(result["candidates"])
        self.assertNotIn("score", result)

    def test_cli_stdin_and_explicit_gate(self):
        script = SKILL / "scripts" / "check.py"
        default = command(script, "-", "--format", "json", stdin="seamless")
        gated = command(script, "-", "--fail-on-candidates", stdin="seamless")
        empty = command(script, "-", "--format", "json", stdin="")
        self.assertEqual((default.returncode, gated.returncode, empty.returncode), (0, 1, 0))
        self.assertEqual(json.loads(default.stdout)["source"], "stdin")
        self.assertEqual(json.loads(empty.stdout)["candidates"], [])

    def test_cli_bad_input_is_error_and_file_scan_does_not_mutate(self):
        with tempfile.TemporaryDirectory() as folder:
            copy = Path(folder) / "text with spaces.md"
            data = b"A seamless trial.\n"
            copy.write_bytes(data)
            result = command(SKILL / "scripts" / "check.py", copy)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(copy.read_bytes(), data)
            copy.write_bytes(b"\xff")
            self.assertEqual(command(SKILL / "scripts" / "check.py", copy).returncode, 2)
        self.assertEqual(command(SKILL / "scripts" / "check.py", "/does/not/exist").returncode, 2)


class ContextTests(unittest.TestCase):
    def test_case_insensitive_scope_and_explicit_brief(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "audience.md").write_text("Teachers")
            (root / ".reader-first").mkdir()
            (root / ".reader-first" / "PRODUCT.md").write_text("Drafts")
            (root / "page.md").write_text("Hero")
            result = context.discover(root, "page.md")
            self.assertEqual(result["records"]["AUDIENCE.md"]["status"], "found")
            self.assertEqual(result["records"]["PRODUCT.md"]["status"], "found")
            self.assertEqual(result["records"]["VOICE.md"]["status"], "missing")
            self.assertEqual(result["brief"], str((root / "page.md").resolve()))

    def test_ambiguity_is_unresolved_and_read_only(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "AUDIENCE.md").write_text("Teachers")
            (root / ".reader-first").mkdir()
            (root / ".reader-first" / "audience.md").write_text("Developers")
            before = {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}
            result = command(SKILL / "scripts" / "load_context.py", "--root", root)
            self.assertEqual(result.returncode, 1)
            record = json.loads(result.stdout)["records"]["AUDIENCE.md"]
            self.assertIsNone(record["path"])
            self.assertEqual(len(record["candidates"]), 2)
            self.assertEqual(before, {p: p.read_bytes() for p in root.rglob("*") if p.is_file()})

    def test_no_parent_fallback_or_external_auto_symlink(self):
        with tempfile.TemporaryDirectory() as folder:
            parent = Path(folder)
            (parent / "PRODUCT.md").write_text("Wrong product")
            child = parent / "app"
            child.mkdir()
            (child / "PRODUCT.md").symlink_to(parent / "PRODUCT.md")
            result = context.discover(child)
            self.assertEqual(result["records"]["PRODUCT.md"]["status"], "missing")
            self.assertTrue(result["warnings"])
            self.assertFalse((child / "AUDIENCE.md").exists())

    def test_external_context_directory_is_error(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / "app"
            root.mkdir()
            (root / ".reader-first").symlink_to(Path(folder), target_is_directory=True)
            with self.assertRaises(ValueError):
                context.discover(root)

    def test_bad_brief_or_root_is_actionable_error(self):
        result = command(SKILL / "scripts" / "load_context.py", "--root", ROOT, "--brief", "missing.md")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Context error", result.stderr)


class InstallTests(unittest.TestCase):
    def test_two_host_layouts_and_isolated_project_scope(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            paths = installer.destinations("both", "project", root)
            self.assertEqual(paths, [root.resolve() / ".agents/skills/reader-first", root.resolve() / ".claude/skills/reader-first"])
            for path in paths:
                self.assertEqual(installer.install(SKILL, path)["status"], "installed")
                self.assertEqual(installer.install(SKILL, path)["status"], "already installed")
                self.assertTrue(installer.identical(SKILL, path))
                self.assertFalse(path.is_symlink())
                self.assertTrue((path / "LICENSE").exists())

    def test_existing_content_survives_refusal_and_update(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "with spaces" / "reader-first"
            target.mkdir(parents=True)
            (target / "custom.md").write_text("User-owned copy")
            with self.assertRaises(ValueError):
                installer.install(SKILL, target)
            self.assertEqual((target / "custom.md").read_text(), "User-owned copy")
            result = installer.install(SKILL, target, update=True)
            backup = Path(result["backup"])
            self.assertEqual((backup / "custom.md").read_text(), "User-owned copy")
            self.assertTrue(installer.identical(SKILL, target))

    def test_symlink_and_overlapping_destination_are_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            real = root / "real"
            real.mkdir()
            link = root / "link"
            link.symlink_to(real, target_is_directory=True)
            with self.assertRaises(ValueError):
                installer.install(SKILL, link, update=True)
            self.assertEqual(list(real.iterdir()), [])
        with self.assertRaises(ValueError):
            installer.install(SKILL, SKILL / "nested")


class DistributionTests(unittest.TestCase):
    def test_markdown_local_links_resolve_and_no_machine_specific_paths(self):
        for path in ROOT.rglob("*.md"):
            if "dist" in path.parts:
                continue
            body = path.read_text(encoding="utf-8")
            self.assertNotIn("/Users/lucasweaver", body, str(path))
            for link in re.findall(r"\]\(([^\s)]+)\)", body):
                if "://" in link or link.startswith("#"):
                    continue
                self.assertTrue((path.parent / link.split("#")[0]).exists(), "{} -> {}".format(path, link))

    def test_archive_installs_and_runs_without_repository(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            archive = packager.build(root / "release.zip")
            original = archive.read_bytes()
            with self.assertRaises(FileExistsError):
                packager.build(archive)
            self.assertEqual(archive.read_bytes(), original)
            with zipfile.ZipFile(archive) as bundle:
                self.assertIsNone(bundle.testzip())
                bundle.extractall(root / "unpacked")
            release = root / "unpacked" / ("reader-first-" + packager.VERSION)
            destination = root / "clean install" / "reader-first"
            result = command(release / "install.py", "--destination", destination, cwd=root)
            self.assertEqual(result.returncode, 0, result.stderr)
            scanned = command(destination / "scripts" / "check.py", "-", "--format", "json", stdin="A seamless platform", cwd=root)
            self.assertEqual(scanned.returncode, 0, scanned.stderr)
            self.assertTrue(json.loads(scanned.stdout)["candidates"])
            tested = command(release / "scripts" / "package.py", "--output", root / "repacked.zip", cwd=root)
            self.assertEqual(tested.returncode, 0, tested.stderr)


if __name__ == "__main__":
    unittest.main()
