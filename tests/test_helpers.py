"""Integration invariants for portable, read-only helper behavior."""

import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "decringe"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = load("decringe_checker", SKILL / "scripts" / "check.py")
context = load("decringe_context", SKILL / "scripts" / "load_context.py")
installer = load("decringe_installer", ROOT / "install.py")
packager = load("decringe_packager", ROOT / "scripts" / "package.py")


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
        result = checker.scan(text, "sample", profile="saas-copy")
        self.assertEqual(text, "PostgreSQL logical replication with at-least-once delivery.")
        self.assertTrue(result["candidates"])
        self.assertNotIn("score", result)

    def test_profiles_always_include_core_and_exclude_other_specialist(self):
        text = "Furthermore, PostgreSQL supports replication. Your draft is safe."
        results = {name: checker.scan(text, "sample", profile=name) for name in checker.PROFILES}
        modules = lambda result: {item["module"] for item in result["candidates"]}
        self.assertEqual(modules(results["core"]), {"core"})
        self.assertEqual(modules(results["saas-copy"]), {"core", "saas-copy"})
        self.assertEqual(modules(results["ui"]), {"core", "ui"})
        self.assertEqual(modules(results["saas-copy+ui"]), {"core", "saas-copy", "ui"})
        core_spans = {(x["start"], x["end"]) for x in results["core"]["candidates"]}
        for result in results.values():
            self.assertEqual(core_spans, {(x["start"], x["end"]) for x in result["candidates"] if x["module"] == "core"})

    def test_same_owner_and_span_emitted_once(self):
        result = checker.scan("Pivotal work. Delve into a vibrant ecosystem.", "sample")
        locations = [(x["module"], x["start"], x["end"]) for x in result["candidates"]]
        self.assertEqual(len(locations), len(set(locations)))
        self.assertEqual(len([x for x in result["candidates"] if x["match"] == "Pivotal"]), 1)

    def test_legacy_cadences_and_count_threshold_remain_available(self):
        text = "Let's be real. By the end of this guide, you'll know. The result? Better words. That's the move."
        rules = {x["rule"] for x in checker.scan(text, "sample")["candidates"]}
        self.assertTrue({"STYLE-04", "STYLE-05", "STYLE-06"}.issubset(rules))
        one = checker.scan("One — aside.", "sample")["candidates"]
        two = checker.scan("One — aside. Two — pauses.", "sample")["candidates"]
        self.assertFalse(any(x["rule"] == "STYLE-08" for x in one))
        self.assertTrue(any(x["rule"] == "STYLE-08" for x in two))

    def test_legacy_json_flag_and_bad_profile(self):
        result = command(SKILL / "scripts" / "check.py", "-", "--json", stdin="Furthermore.")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["schema_version"], 2)
        self.assertEqual(command(SKILL / "scripts" / "check.py", "-", "--profile", "missing", stdin="").returncode, 2)

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
    def test_legacy_context_remains_readable_and_conflicts_are_ambiguous(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            legacy = root / ".reader-first"
            legacy.mkdir()
            (legacy / "AUDIENCE.md").write_text("Teachers")
            self.assertEqual(context.discover(root)["records"]["AUDIENCE.md"]["status"], "found")
            modern = root / ".decringe"
            modern.mkdir()
            (modern / "AUDIENCE.md").write_text("Developers")
            result = context.discover(root)["records"]["AUDIENCE.md"]
            self.assertEqual(result["status"], "ambiguous")
            self.assertIsNone(result["path"])

    def test_case_insensitive_scope_and_explicit_brief(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "audience.md").write_text("Teachers")
            (root / ".decringe").mkdir()
            (root / ".decringe" / "PRODUCT.md").write_text("Drafts")
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
            (root / ".decringe").mkdir()
            (root / ".decringe" / "audience.md").write_text("Developers")
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
            (root / ".decringe").symlink_to(Path(folder), target_is_directory=True)
            with self.assertRaises(ValueError):
                context.discover(root)

    def test_bad_brief_or_root_is_actionable_error(self):
        result = command(SKILL / "scripts" / "load_context.py", "--root", ROOT, "--brief", "missing.md")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Context error", result.stderr)


class InstallTests(unittest.TestCase):
    def test_failed_replacement_restores_previous_install(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "skills/decringe"
            target.mkdir(parents=True)
            (target / "custom.md").write_text("Preserve this")
            original_rename = Path.rename

            def rename(path, destination):
                if path.parent.name.startswith(".decringe-stage-"):
                    raise OSError("Simulated final rename failure")
                return original_rename(path, destination)

            with mock.patch.object(Path, "rename", rename):
                with self.assertRaises(OSError):
                    installer.install(SKILL, target, update=True)
            self.assertEqual((target / "custom.md").read_text(), "Preserve this")

    def test_migration_keeps_backups_and_alias_has_no_rule_catalog(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            target = home / ".agents/skills/decringe"
            installer.install(SKILL, target)
            reader = target.parent / "reader-first"
            reader.mkdir()
            (reader / "SKILL.md").write_text("Old reader skill")
            alias = target.parent / "decontaminate"
            alias.mkdir()
            (alias / "SKILL.md").write_text("Old cleanup skill")
            (alias / "rules.md").write_text("Old independent rules")
            legacy = home / ".codex/skills/decringe"
            legacy.mkdir(parents=True)
            (legacy / "SKILL.md").write_text("Old decringe")
            changes = installer.migrate_legacy(target, legacy)
            self.assertFalse(reader.exists())
            self.assertFalse((legacy / "SKILL.md").exists())
            self.assertFalse((alias / "rules.md").exists())
            preserved = [Path(x["backup"]) for x in changes if x.get("backup")]
            self.assertEqual(len(preserved), 3)
            self.assertTrue(any((p / "rules.md").exists() for p in preserved))
            self.assertTrue(all(p.parent.name == "decringe-backups" for p in preserved))
            scanned = command(alias / "check.py", "-", "--json", stdin="Pivotal work.")
            self.assertEqual(scanned.returncode, 1, scanned.stderr)
            self.assertEqual(json.loads(scanned.stdout)["profile"], "core")
            old_path = command(legacy / "scripts/check.py", "-", "--json", stdin="Pivotal work.")
            self.assertEqual(old_path.returncode, 1, old_path.stderr)
            self.assertEqual(json.loads(old_path.stdout)["candidates"], json.loads(scanned.stdout)["candidates"])
            repeated = installer.migrate_legacy(target, legacy)
            self.assertTrue(all(not x.get("backup") for x in repeated))

    def test_two_host_layouts_and_isolated_project_scope(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            paths = installer.destinations("both", "project", root)
            self.assertEqual(paths, [root.resolve() / ".agents/skills/decringe", root.resolve() / ".claude/skills/decringe"])
            for path in paths:
                self.assertEqual(installer.install(SKILL, path)["status"], "installed")
                self.assertEqual(installer.install(SKILL, path)["status"], "already installed")
                self.assertTrue(installer.identical(SKILL, path))
                self.assertFalse(path.is_symlink())
                self.assertTrue((path / "LICENSE").exists())

    def test_existing_content_survives_refusal_and_update(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "with spaces" / "decringe"
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
            release = root / "unpacked" / ("decringe-" + packager.VERSION)
            destination = root / "clean install" / "decringe"
            result = command(release / "install.py", "--destination", destination, cwd=root)
            self.assertEqual(result.returncode, 0, result.stderr)
            scanned = command(destination / "scripts" / "check.py", "-", "--format", "json", stdin="A seamless platform", cwd=root)
            self.assertEqual(scanned.returncode, 0, scanned.stderr)
            self.assertTrue(json.loads(scanned.stdout)["candidates"])
            tested = command(release / "scripts" / "package.py", "--output", root / "repacked.zip", cwd=root)
            self.assertEqual(tested.returncode, 0, tested.stderr)


if __name__ == "__main__":
    unittest.main()
