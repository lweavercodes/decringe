#!/usr/bin/env python3
"""Forward the legacy offline scanner path to the canonical Decringe scanner."""

from pathlib import Path
import runpy
import sys


target = Path(__file__).resolve().parent.parent / "decringe" / "scripts" / "check.py"
if not target.is_file():
    print("Missing sibling decringe skill; install the canonical skill first.", file=sys.stderr)
    sys.exit(2)
# Preserve the old candidate-present exit status for legacy script callers.
sys.argv[0] = str(target)
sys.argv.append("--fail-on-candidates")
runpy.run_path(str(target), run_name="__main__")
