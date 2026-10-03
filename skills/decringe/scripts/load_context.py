#!/usr/bin/env python3
"""Report context paths within one explicitly selected project. Read-only."""

import argparse
import json
from pathlib import Path
import sys


RECORDS = ("AUDIENCE.md", "PRODUCT.md", "VOICE.md")


def discover(root, brief=None):
    root = Path(root).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Project root must be a directory")
    folders = [root]
    for name in (".decringe", ".reader-first"):
        optional = root / name
        if optional.exists():
            resolved = optional.resolve()
            if not resolved.is_relative_to(root) or not resolved.is_dir():
                raise ValueError("{} must be a directory inside the selected project".format(name))
            folders.append(optional)
    records, warnings = {}, []
    for name in RECORDS:
        matches = []
        for folder in folders:
            for path in sorted(folder.iterdir()):
                if path.name.casefold() != name.casefold() or not path.is_file():
                    continue
                resolved = path.resolve(strict=True)
                if not resolved.is_relative_to(root):
                    warnings.append("Ignored context outside project: {}".format(path))
                    continue
                matches.append(str(path))
        records[name] = {
            "status": "ambiguous" if len(matches) > 1 else ("found" if matches else "missing"),
            "path": matches[0] if len(matches) == 1 else None,
            "candidates": matches,
        }
    brief_path = None
    if brief:
        supplied = Path(brief).expanduser()
        supplied = supplied if supplied.is_absolute() else root / supplied
        supplied = supplied.resolve(strict=True)
        if not supplied.is_file() or supplied.suffix.lower() != ".md":
            raise ValueError("Brief must be an existing Markdown file")
        brief_path = str(supplied)
    return {"schema_version": 1, "root": str(root), "records": records, "brief": brief_path, "warnings": warnings}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Selected app/project root; no parent fallback")
    parser.add_argument("--brief", help="Explicit Markdown brief, relative to root or absolute")
    args = parser.parse_args(argv)
    try:
        result = discover(args.root, args.brief)
    except (OSError, ValueError, RuntimeError) as error:
        print("Context error: {}".format(error), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if any(record["status"] == "ambiguous" for record in result["records"].values()) else 0


if __name__ == "__main__":
    sys.exit(main())
