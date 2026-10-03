#!/usr/bin/env python3
"""Build a portable archive from a fixed release file set."""

import argparse
from pathlib import Path
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.2.1"


def build(output):
    output = Path(output)
    files = [ROOT / name for name in ("README.md", "LICENSE", "CONTRIBUTING.md", "AGENTS.md", "install.py")]
    for folder in ("skills", "compat", "docs", "examples", "tests", "scripts"):
        files += [p for p in (ROOT / folder).rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc" and p.name != ".decringe-source.json"]
    if any(p.is_symlink() for p in files):
        raise ValueError("Release files must not be symlinks")
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(files):
                archive.write(path, Path("decringe-" + VERSION) / path.relative_to(ROOT))
    except Exception:
        # A pre-existing archive must survive a failed exclusive open.
        if "archive" in locals():
            output.unlink(missing_ok=True)
        raise
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=str(ROOT / "dist" / ("decringe-" + VERSION + ".zip")))
    args = parser.parse_args(argv)
    try:
        print(build(args.output))
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print("Package error: {}".format(error), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
