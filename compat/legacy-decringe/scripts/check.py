#!/usr/bin/env python3
"""Preserve the old user-level .codex scanner path without another skill entry."""

from pathlib import Path
import runpy
import sys


target = Path(__file__).resolve().parents[4] / ".agents" / "skills" / "decringe" / "scripts" / "check.py"
if not target.is_file():
    print("Missing canonical .agents decringe install.", file=sys.stderr)
    sys.exit(2)
sys.argv[0] = str(target)
sys.argv.append("--fail-on-candidates")
runpy.run_path(str(target), run_name="__main__")
