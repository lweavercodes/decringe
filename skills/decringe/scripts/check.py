#!/usr/bin/env python3
"""Find editorial candidates in prose. No network, model calls, or mutations."""

import argparse
import bisect
import json
from pathlib import Path
import re
import sys


PATTERNS = Path(__file__).resolve().parents[1] / "references" / "patterns.json"
PROFILES = {
    "core": {"core"},
    "saas-copy": {"core", "saas-copy"},
    "ui": {"core", "ui"},
    "saas-copy+ui": {"core", "saas-copy", "ui"},
}


def mask_markdown(text):
    """Hide common non-prose regions without changing character offsets."""
    masked = list(text)

    def hide(start, end):
        for pos in range(start, end):
            if text[pos] not in "\r\n":
                masked[pos] = " "

    fence = None
    offset = 0
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if fence:
            hide(offset, offset + len(line))
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= fence[1] and not marker[2].strip():
                fence = None
        elif marker and not (marker[1][0] == "`" and "`" in marker[2]):
            fence = (marker[1][0], len(marker[1]))
            hide(offset, offset + len(line))
        elif line.startswith(("    ", "\t")):
            hide(offset, offset + len(line))
        offset += len(line)

    for pattern in (
        r"<!--.*?(?:-->|\Z)",
        r"(?<!`)(`+)(?!`)(?:[^`]|(?!\1)`)*?\1(?!`)",
        r"\]\((?:[^()\n]|\([^()\n]*\))*\)",
        r"(?m)^ {0,3}\[[^\]\n]+\]:[^\n]*",
        r"https?://[^\s<>]+",
    ):
        for match in re.finditer(pattern, "".join(masked), re.DOTALL):
            hide(match.start(), match.end())
    return "".join(masked)


def scan(text, source, patterns_path=PATTERNS, profile="core"):
    if profile not in PROFILES:
        raise ValueError("Unknown profile: {}".format(profile))
    config = json.loads(patterns_path.read_text(encoding="utf-8"))
    visible = mask_markdown(text)
    line_starts = [0] + [m.end() for m in re.finditer(r"\n", text)]
    candidates = []
    seen = set()
    for pattern in config["patterns"]:
        owner = pattern["module"]
        if owner not in PROFILES[profile]:
            continue
        matches = list(re.finditer(pattern["regex"], visible, re.IGNORECASE))
        if pattern.get("kind") == "count_regex" and len(matches) < pattern["threshold"]:
            continue
        for match in matches:
            location = (owner, match.start(), match.end())
            if location in seen:
                continue
            seen.add(location)
            line_index = bisect.bisect_right(line_starts, match.start()) - 1
            candidates.append({
                "module": owner,
                "rule": pattern["rule"],
                "candidate": pattern["candidate"],
                "match": text[match.start():match.end()],
                "line": line_index + 1,
                "column": match.start() - line_starts[line_index] + 1,
                "start": match.start(),
                "end": match.end(),
            })
    candidates.sort(key=lambda item: (item["start"], item["rule"]))
    return {
        "schema_version": 2,
        "source": source,
        "profile": profile,
        "modules": sorted(PROFILES[profile]),
        "candidates": candidates,
        "summary": {"candidate_count": len(candidates), "contextual_review_required": True},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="UTF-8 text/Markdown path, or - for stdin")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--json", action="store_true", help="Compatibility alias for --format json")
    parser.add_argument("--profile", choices=tuple(PROFILES), default="core")
    parser.add_argument("--fail-on-candidates", action="store_true")
    args = parser.parse_args(argv)
    try:
        text = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
        result = scan(text, "stdin" if args.file == "-" else args.file, profile=args.profile)
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, re.error) as error:
        print("Scanner error: {}".format(error), file=sys.stderr)
        return 2
    if args.format == "json" or args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for item in result["candidates"]:
            print("{source}:{line}:{column} [{module}/{rule}] {match!r}: {candidate}".format(source=result["source"], **item))
        print("{} candidate(s); contextual review still required.".format(len(result["candidates"])))
    return 1 if args.fail_on_candidates and result["candidates"] else 0


if __name__ == "__main__":
    sys.exit(main())
