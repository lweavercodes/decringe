# Contributing

Bring a reproducible writing failure, its reader and product context, and a smallest useful repair. Redact customer and private project details.

For a rule change, explain the reader misunderstanding, the evidence supporting the repair, and an example where the original wording should remain. Preserve existing IDs; use a new ID for a new substantive rule. Avoid global banned-word lists and growing the entrypoint with examples that belong in references.

For helper changes, keep Python 3.9+ and standard-library-only operation. Preserve read-only scanner/context behavior, Unicode positions, bounded context scope, and install backups. Run `python3 -B -m unittest discover -s tests -v`, then exercise the relevant cases in [docs/evaluation.md](docs/evaluation.md) with a fresh agent session when available.

Do not claim a model benchmark from a deterministic test suite or one successful rewrite. Report the environment, inputs, observed decisions, and limitations. New release versions should update the version in `scripts/package.py` and README together.
