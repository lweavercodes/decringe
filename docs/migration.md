# Migration to Decringe v0.2

The public skill is now `decringe`. The initial Reader First name is retired. There is one canonical core, with `saas-copy` and `ui` modules; operations remain independent of modules.

## Install and consolidate

`python3 install.py --target both --update --migrate-legacy` installs canonical copies into the selected Codex and Claude Code user directories. Project installs also support migration within the selected project. An explicit `--destination` limits migration to sibling installs there. The default installer does not retire other skills.

After canonical installation, explicit migration:

1. Moves a sibling `reader-first` directory to a timestamped backup outside skill discovery.
2. Replaces an existing sibling `decontaminate` with the thin compatibility alias, preserving its previous contents first. New users do not receive the alias unless migrating an existing installation.
3. For default user-level Codex installation, archives an existing `~/.codex/skills/decringe` skill and leaves only scanner forwarding scripts at its old paths. Canonical discovery uses `~/.agents/skills/decringe`.

Backups live in `decringe-backups/` beside the relevant `skills/` directory. Exact paths are printed. No backup is deleted; previous API scripts and model settings remain available in those snapshots. Symlink destinations are refused rather than followed or replaced. If a step fails, the installer reports the failure; earlier successful installations/migrations may remain and their backups are still available. Rerunning is safe for identical copies and already-retired entries.

## Compatibility scope

- Existing explicit `decontaminate` requests load the sibling canonical skill. The alias owns no writing rules. Codex implicit selection is disabled in its UI metadata; Claude uses its documented `disable-model-invocation` field. See [Claude invocation controls](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill).
- Legacy offline scanner paths forward to the canonical script, accept `--json`, and retain candidate-present exit code 1. They do not preserve the old JSON schema or API-backed semantic flags.
- New scanner output is schema version 2 with an owner and selected profile. Update any consumer that parses old scanner JSON. `--semantic`/`--voice` API flags fail explicitly; contextual/voice review follows the explicit lightweight-subagent protocol with the complete bundled rulebook. Host restrictions require disclosed self-review rather than silently switching models.
- Existing `.reader-first/` context is readable alongside `.decringe/`. Conflicting records are flagged; no context file is automatically renamed or merged.

## Native workflows

Change a workflow's authored-output review step to invoke canonical Decringe with the relevant module. General prose uses core; SaaS marketing uses `saas-copy`; interface text uses `ui`; mixed surfaces select both. Keep one review and one coherent edit rather than stacking independent writers.

For a native application without installed skill discovery, vendor the canonical `skills/decringe` directory and explicitly load SKILL.md and its selected relative references. Do not copy a second rules list into the application prompt. Helpers work offline; the workflow's existing agent performs contextual judgment. Deployment and any application's data/configuration migration are outside this package's local skill migration.
