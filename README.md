# Decringe

An open writing skill for Codex and Claude Code: a decontamination core with focused `saas-copy` and `ui` modules.

[Source and change history](https://github.com/lweavercodes/decringe) · [Releases](https://github.com/lweavercodes/decringe/releases)

Decringe helps your agent explain the product in the reader's language, check promises against product facts, and write UI text that matches what actually happens. It also removes canned rhetoric and empty praise while preserving useful voice and technical precision.

**Example:** A teacher does not need “multi-tenant orchestration with a RAG pipeline.” They need to know they can turn lesson notes into a worksheet draft, edit it, and assign it. That translation still needs product evidence: a background queue does not prove the teacher saves three hours.

## Install

Download/unpack this repository or its release ZIP, then run the installer from that folder. Python 3.9+ is required for the installer and optional helpers; the Markdown skill works without Python.

```sh
python3 install.py --target both
```

This copies a self-contained skill to:

- Codex: `~/.agents/skills/decringe/`
- Claude Code: `~/.claude/skills/decringe/`

Use `--target codex` or `--target claude` for one environment. To share it inside a project:

```sh
python3 install.py --target both --scope project --project /path/to/project
```

The project locations are `.agents/skills/decringe/` and `.claude/skills/decringe/`. Commit the installed directory if you want teammates to receive it. Installation does not create context documents or change project instructions. A different existing installation is preserved unless you pass `--update`; that option backs it up before replacing it. Backups go in a `decringe-backups` directory beside the `skills` directory, and the installer prints the exact path. Identical installs are a no-op. A custom final directory is supported with `--destination /path/to/skills/decringe`.

Manual installation also works: copy **the entire** `skills/decringe` directory into either environment's skills directory. No symlinks, other skills, API key, Wordflows account, model pin, or network service is required.

The installer also writes a local `.decringe-source.json` hint inside the canonical install, pointing agents to its editable source. It is excluded from releases and ignored by Git; omit it when sharing an installed directory. Manual copies work without it.

These are local agent installs. Web chats and cloud environments need their own supported upload/plugin mechanism. Check the current [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skill documentation](https://code.claude.com/docs/en/skills) if your environment uses a different layout. If the skill does not appear after installation, start a new session.

## Use

In Codex:

```text
$decringe init
$decringe this draft while keeping its meaning
$decringe saas-copy audit our homepage messaging
$decringe saas-copy rewrite this hero for independent teachers
$decringe ui write an empty state for the worksheet list
$decringe ui distill this onboarding message to 120 characters
$decringe saas-copy adapt this page for developer buyers
$decringe saas-copy+ui audit this complete landing page
$decringe improve this observed failure in our UI review
```

In Claude Code, use `/decringe` with the same arguments. These are arguments to one skill, not separately installed commands. Modules select expertise; operations (`audit`, `write`, `rewrite`, `distill`, `adapt`) select the work. Bare Decringe performs core cleanup. If no module is specified, the agent infers specialist coverage from the requested task. `init` records shared context.

| Module | Owns | Always includes |
| --- | --- | --- |
| `core` | AI words, canned rhetoric, empty praise, synthetic cadence and voice preservation | Shared truth/scope constraints |
| `saas-copy` | Offer, reader relevance, differentiation, proof, pricing and buyer commitment | Core and shared constraints |
| `ui` | Controls, labels, forms, states, action consequences and recovery | Core and shared constraints |
| `saas-copy+ui` | Marketing sections plus controls on a mixed surface | Core and shared constraints |

Each rule has one owner. A complete page can use both modules on different spans, then receive one coherent edit and final core check. UI owns whether a button actually starts a trial; SaaS owns whether the page explains the trial's material conditions. See the [ownership index](skills/decringe/references/rules.md).

For a quick edit, paste the text and explain the reader and relevant behavior. Setup is optional. `audit` reports findings without changing files; `write` and `rewrite` produce or edit the requested copy. None of the modes authorizes publishing or changing product behavior.

## Teach it your project

`init` uses what your agent can establish from the conversation and relevant project material to save reusable context. Unknowns remain marked; it should ask only for a fact that changes the result.

| File | Purpose |
| --- | --- |
| `AUDIENCE.md` | Reader situations, tasks, vocabulary, and evidence |
| `PRODUCT.md` | Verified capabilities, offer, limits, actions, and proof |
| `VOICE.md` | Optional approved voice examples and terminology |
| `.decringe/briefs/<surface>.md` | Optional page/flow brief selecting an audience and next action |

Files may live at the selected app root or under `.decringe/`. Existing `.reader-first/` context is recognized without automatic migration. Existing equivalent records are reusable; `audience.md` is recognized too. Conflicting files are flagged, and the loader never silently inherits another app's context. If you already use Impeccable, keep its compatible `PRODUCT.md`; visual `DESIGN.md` stays separate.

Start with the [templates](skills/decringe/assets/templates/) or the complete [fictional example](examples/lesson-draft/). The [context guide](skills/decringe/references/context.md) explains ownership, evidence, and resolution.

## What it checks

- Technical implementation used where the reader needs a task or offer.
- Feature lists, interchangeable benefits, unclear positioning, and repeated sections.
- Unsupported outcomes, manufactured proof, invented customer psychology, and CTA mismatches.
- Internal UI terms, inaccurate states, invented error causes, and incorrect recovery or deletion promises.
- Canned contrasts, inflated significance, empty intensifiers, and repetitive AI cadence.

The [ownership index](skills/decringe/references/rules.md) links to canonical module rules and exceptions. Developer audiences sometimes need technical detail; a verified trial can say “no card required”; an effective contrast or em dash can stay. Decringe reviews usefulness and truth, not authorship.

## Optional helpers

From the repository:

```sh
python3 skills/decringe/scripts/check.py examples/lesson-draft/before.md --profile saas-copy+ui --format json
python3 skills/decringe/scripts/load_context.py --root examples/lesson-draft --brief BRIEF.md
```

The scanner finds candidates in plain text/Markdown. Default profile is `core`; every specialist profile includes core patterns and excludes the unselected specialist. It does not evaluate the audience, verify claims, parse application source, or score AI probability. Zero candidates still requires contextual review. The [scanner contract](skills/decringe/references/scanner.md) documents formats, masking, offsets, and exit codes. Installed helpers live inside the installed skill's `scripts/` directory.

## Existing installations and workflows

To replace older versions and consolidate existing Reader First/decontaminate installs:

```sh
python3 install.py --target both --update --migrate-legacy
```

Migration is opt-in. It preserves retired files in backups outside skill discovery, retires `reader-first`, and replaces an existing `decontaminate` with a thin explicit compatibility alias. The alias forwards to sibling Decringe and owns no rules. User-level Codex migration preserves old `.codex/skills/decringe` scanner paths as forwarding scripts without a duplicate skill entry. New installs need only the canonical folder. See [migration.md](docs/migration.md).

Native content workflows should explicitly invoke Decringe before returning authored output, selecting `saas-copy`, `ui`, or core as appropriate. Every invocation includes core; automatic skill selection alone is not enforcement. This package does not change a workflow application's deployed behavior.

## Improve the skill

There is a [rules.md](skills/decringe/references/rules.md): it indexes rule ownership and links to the canonical core, SaaS and UI guidance. The [maintenance guide](skills/decringe/references/maintenance.md) maps editable files and describes the bounded improvement loop: observed failure → cause/owner → focused change → failure and preservation cases → regressions → commit → refresh copies.

Edit the source checkout's `skills/decringe/` Markdown rather than only an installed copy. SKILL.md points agents to the repository and optional local source hint. Use the [improvement case template](skills/decringe/assets/templates/IMPROVEMENT_CASE.md) to record redacted evidence and actual evaluation results. Ordinary copy work does not silently rewrite the skill; `improve` is for an authorized skill change. Fewer scanner hits or the agent liking its own rewrite is not evidence of a better rule.

## Development and release

```sh
python3 -B -m unittest discover -s tests -v
python3 scripts/package.py
```

The package command creates `dist/decringe-0.2.1.zip` and refuses to overwrite an existing archive. Tests exercise candidate locations, Markdown masking, context ambiguity/isolation, install preservation, and portable packaging. [Behavioral evaluation cases](docs/evaluation.md) cover decisions a regex cannot test. [Research and product rationale](docs/research.md) explain the evidence and its limits.

Change substantive writing rules only when a real failure supports the change. New scanner patterns should be cues for contextual review, accompanied by a false-positive example. Preserve stable rule IDs. Contribution guidance is in [CONTRIBUTING.md](CONTRIBUTING.md).

## License and inspiration

MIT, copyright Lucas Weaver. The installed skill includes the license so it can be redistributed on its own.

Inspired by [Impeccable](https://impeccable.style/)'s focused commands and reusable context, and by the decontaminate/decringe approach of scanning candidates followed by judgment. The canonical Decringe package is self-contained. Legacy decringe patterns are consolidated into its core; Impeccable remains an inspiration rather than a runtime dependency. It makes no guarantee about conversion, detection avoidance, or flawless model behavior.
