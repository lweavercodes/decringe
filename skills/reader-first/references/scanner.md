# Scanner contract

`scripts/check.py` is a read-only candidate finder using the Python standard library (Python 3.9+). It calls no models, reads no environment secrets, and makes no network requests. The host agent supplies contextual judgment.

```sh
python3 <skill-dir>/scripts/check.py copy.md
python3 <skill-dir>/scripts/check.py copy.md --format json
python3 <skill-dir>/scripts/check.py - --format json
```

With `-`, supply visible text on stdin. The file format is UTF-8 plain text or Markdown, not an AST of JSX/Svelte/HTML. For UI source, the agent should inspect/extract visible strings and their state separately. Do not edit source based on scanner offsets from an extraction.

The scanner masks fenced and indented Markdown code blocks, inline code, HTML comments, and URL/link destinations while preserving offsets. Link labels remain visible. It does not render HTML, parse localization functions, identify all Markdown nesting, or verify claims. Scan actual displayed technical text as plain prose when it needs review; masking code examples is not an assertion that they are correct.

JSON returns `schema_version`, `source`, `candidates`, and `summary`. Each candidate contains a stable `rule`, a description, the exact `match`, a one-based `line` and `column`, and zero-based Python Unicode `start`/`end` offsets into the supplied text (end exclusive). These are character offsets, not UTF-8 byte positions. Rules and candidate patterns live in `references/rules.md` and `references/patterns.json` respectively.

Default exit code is `0` for a completed scan, with or without candidates. `--fail-on-candidates` returns `1` when candidates exist; it is an optional editorial queue gate, not a quality assessment. Input/configuration errors return `2` with a message on stderr. Empty input succeeds with an empty candidate list.

The patterns are intentionally conservative search cues. False positives are expected: a developer-facing PostgreSQL feature, a legitimate free trial, or a literal use of “seamless” can be correct. False negatives are expected too: a vague offer, omitted prerequisite, fabricated quote, or a misleading “Done” may trigger no pattern. Do not use count reductions as evidence of better copy, authorship, or conversion.

The context loader separately reports named context records. It does not determine whether a blank template contains useful context; the agent must read and assess it. Ambiguous candidates are returned as unresolved, never picked alphabetically. Loader exit codes: `0` resolved/discovered (missing records are allowed), `1` ambiguities, `2` bad root/brief or I/O error.
