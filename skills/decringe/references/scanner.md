# Scanner contract

`scripts/check.py` is a read-only candidate finder using the Python standard library (Python 3.9+). It calls no models, reads no environment secrets, and makes no network requests. The host agent supplies contextual judgment.

```sh
python3 <skill-dir>/scripts/check.py copy.md
python3 <skill-dir>/scripts/check.py copy.md --profile saas-copy --format json
python3 <skill-dir>/scripts/check.py - --format json
```

With `-`, supply visible text on stdin. The file format is UTF-8 plain text or Markdown, not an AST of JSX/Svelte/HTML. For UI source, the agent should inspect/extract visible strings and their state separately. Do not edit source based on scanner offsets from an extraction.

The scanner masks fenced and indented Markdown code blocks, inline code, HTML comments, and URL/link destinations while preserving offsets. Link labels remain visible. It does not render HTML, parse localization functions, identify all Markdown nesting, or verify claims. Scan actual displayed technical text as plain prose when it needs review; masking code examples is not an assertion that they are correct.

JSON schema version 2 returns `schema_version`, `source`, `profile`, `modules`, `candidates`, and `summary`. Each candidate contains its owning `module`, a stable `rule`, a description, the exact `match`, a one-based `line` and `column`, and zero-based Python Unicode `start`/`end` offsets into the supplied text (end exclusive). These are character offsets, not UTF-8 byte positions. The ownership index lives in `references/rules.md`, canonical rules live in their module references, and candidate patterns live once in `references/patterns.json`.

Default exit code is `0` for a completed scan, with or without candidates. `--fail-on-candidates` returns `1` when candidates exist; it is an optional editorial queue gate, not a quality assessment. Input/configuration errors return `2` with a message on stderr. Empty input succeeds with an empty candidate list.

The patterns are intentionally conservative search cues. False positives are expected: a developer-facing PostgreSQL feature, a legitimate free trial, or a literal use of “seamless” can be correct. False negatives are expected too: a vague offer, omitted prerequisite, fabricated quote, or a misleading “Done” may trigger no pattern. Do not use count reductions as evidence of better copy, authorship, or conversion.

The context loader separately reports named context records. It does not determine whether a blank template contains useful context; the agent must read and assess it. Ambiguous candidates are returned as unresolved, never picked alphabetically. Loader exit codes: `0` resolved/discovered (missing records are allowed), `1` ambiguities, `2` bad root/brief or I/O error.

## Module filters and compatibility

`--profile core` is the default. `--profile saas-copy`, `--profile ui`, and `--profile saas-copy+ui` add the selected specialist(s), always retaining core. Profiles select cues, not an automatic verdict or routing for every span: contextual review must map controls to UI and marketing text to SaaS. Exact duplicate locations within one owner are emitted once; the agent consolidates overlapping or cross-owner cues into a single substantive finding where appropriate.

`--json` remains an alias for `--format json`. Count-based cadence candidates such as repeated em-dash pauses appear only when the configured threshold is met, and still need judgment. Legacy forwarding scripts add `--fail-on-candidates` to preserve their old exit status. API-backed `--semantic` and `--voice` flags are not implemented by the offline scanner; contextual/voice review belongs to the host agent. No model choice is silently substituted.

The context loader also recognizes `.reader-first/` records for migration compatibility. Conflicts with `.decringe/` remain ambiguous; it does not rename files or silently prefer the new folder.
