#!/usr/bin/env python3
"""Install a self-contained Decringe skill into local Codex or Claude Code."""

import argparse
from datetime import datetime, timezone
import filecmp
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import uuid


SOURCE = Path(__file__).resolve().parent / "skills" / "decringe"
COMPAT = Path(__file__).resolve().parent / "compat"
SOURCE_RECORD = ".decringe-source.json"
REPOSITORY = "https://github.com/lweavercodes/decringe"


def record_source(source, destination):
    """Keep machine-specific editing locations in the installed copy only."""
    if source.name != "decringe":
        return
    root = source.parent.parent
    metadata = {
        "schema_version": 1,
        "repository": REPOSITORY,
        "source_directory": str(root),
        "editable_skill_directory": str(source),
        "is_git_checkout": (root / ".git").exists(),
    }
    (destination / SOURCE_RECORD).write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


def archive(directory):
    """Move a retired install outside skill discovery, preserving all its files."""
    directory = Path(directory)
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError("Refusing to archive a symlink or non-directory: {}".format(directory))
    suffix = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    backup = directory.parent.parent / "decringe-backups" / (directory.name + "-" + suffix)
    backup.parent.mkdir(parents=True, exist_ok=True)
    directory.rename(backup)
    return backup


def release_files(directory):
    return {p.relative_to(directory) for p in directory.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc" and p.name != ".DS_Store" and p.relative_to(directory) != Path(SOURCE_RECORD)}


def identical(source, destination):
    if not destination.is_dir():
        return False
    source_files = release_files(source)
    dest_files = release_files(destination)
    if source_files != dest_files:
        return False
    return all(filecmp.cmp(source / name, destination / name, shallow=False) for name in source_files)


def install(source, destination, update=False):
    source = Path(source).resolve(strict=True)
    if not source.is_dir() or not (source / "SKILL.md").is_file():
        raise ValueError("Source must be a skill directory containing SKILL.md")
    destination = Path(os.path.abspath(Path(destination).expanduser()))
    if destination.is_symlink():
        raise ValueError("Refusing to replace a symlink: {}".format(destination))
    if destination.resolve().is_relative_to(source) or source.is_relative_to(destination.resolve()):
        raise ValueError("Install destination must be separate from the skill source")
    if any(path.is_symlink() for path in source.rglob("*")):
        raise ValueError("Skill source must be a self-contained directory without symlinks")
    if destination.exists():
        if any(path.is_symlink() for path in destination.rglob("*")):
            raise ValueError("Installed directory contains symlinks; resolve them before updating")
        if identical(source, destination):
            record_source(source, destination)
            return {"destination": str(destination), "status": "already installed", "backup": None}
        if not update:
            raise ValueError("Destination exists with different content; use --update to preserve it in a backup: {}".format(destination))
        if not destination.is_dir():
            raise ValueError("Destination must be a directory: {}".format(destination))
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".decringe-stage-", dir=destination.parent))
    backup = None
    try:
        shutil.copytree(source, stage / "decringe", ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", SOURCE_RECORD))
        record_source(source, stage / "decringe")
        if destination.exists():
            backup = archive(destination)
        try:
            (stage / "decringe").rename(destination)
        except OSError:
            if backup:
                backup.rename(destination)
            raise
    finally:
        shutil.rmtree(stage)
    return {"destination": str(destination), "status": "installed", "backup": str(backup) if backup else None}


def migrate_legacy(destination, legacy_codex=None):
    """Explicit migration only; canonical install must already be present."""
    destination = Path(destination)
    if not (destination / "SKILL.md").is_file():
        raise ValueError("Canonical skill must be installed before migration")
    changes = []
    old_reader = destination.parent / "reader-first"
    if old_reader.exists() or old_reader.is_symlink():
        changes.append({"retired": str(old_reader), "backup": str(archive(old_reader))})
    alias = destination.parent / "decontaminate"
    if alias.exists() or alias.is_symlink():
        changes.append(install(COMPAT / "decontaminate", alias, update=True))
    if legacy_codex:
        legacy = Path(legacy_codex)
        if (legacy / "SKILL.md").exists():
            backup = archive(legacy)
            try:
                shutil.copytree(COMPAT / "legacy-decringe", legacy)
            except OSError:
                if legacy.exists():
                    shutil.rmtree(legacy)
                backup.rename(legacy)
                raise
            changes.append({"retired": str(legacy), "backup": str(backup), "compatibility": "scanner paths only"})
    return changes


def destinations(target, scope, project=None, home=None):
    base = Path(home) if home else Path.home()
    if scope == "project":
        if not project:
            raise ValueError("--project is required with --scope project")
        base = Path(project).expanduser().resolve(strict=True)
        if not base.is_dir():
            raise ValueError("Project must be an existing directory")
    folders = {"codex": ".agents", "claude": ".claude"}
    choices = folders if target == "both" else [target]
    return [base / folders[name] / "skills" / "decringe" for name in choices]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=("codex", "claude", "both"), default="both")
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument("--project", help="Project directory (required for project scope)")
    parser.add_argument("--destination", help="Explicit final skill directory; overrides target/scope")
    parser.add_argument("--update", action="store_true", help="Back up a different existing install before replacing")
    parser.add_argument("--migrate-legacy", action="store_true", help="Archive Reader First, replace existing decontaminate with an alias, and migrate user .codex/decringe")
    args = parser.parse_args(argv)
    try:
        paths = [Path(args.destination)] if args.destination else destinations(args.target, args.scope, args.project)
        for path in paths:
            result = install(SOURCE, path, args.update)
            print("{}: {}".format(result["status"], result["destination"]))
            if result["backup"]:
                print("Previous install preserved: {}".format(result["backup"]))
            if args.migrate_legacy:
                legacy_codex = None
                if not args.destination and args.scope == "user" and path.parent.parent.name == ".agents":
                    legacy_codex = Path.home() / ".codex" / "skills" / "decringe"
                for change in migrate_legacy(path, legacy_codex):
                    print("Migration: {}".format(change))
    except (OSError, ValueError, RuntimeError) as error:
        print("Install error: {}".format(error), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
