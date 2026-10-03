#!/usr/bin/env python3
"""Forward the old root-level scanner path."""

from pathlib import Path
import runpy


runpy.run_path(str(Path(__file__).resolve().parent / "scripts" / "check.py"), run_name="__main__")
