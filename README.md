# Reader First

An open skill for copywriting and UX text in Codex and Claude Code.

Reader First helps your agent explain the product in the reader's language, check promises against product facts, and write UI text that matches what actually happens. It also removes canned rhetoric and empty praise while preserving useful voice and technical precision.

**Example:** A teacher does not need “multi-tenant orchestration with a RAG pipeline.” They need to know they can turn lesson notes into a worksheet draft, edit it, and assign it. That translation still needs product evidence: a background queue does not prove the teacher saves three hours.

## Install

Download/unpack this repository or its release ZIP, then run the installer from that folder. Python 3.9+ is required for the installer and optional helpers; the Markdown skill works without Python.

```sh
python3 install.py --target both
```

This copies a self-contained skill to:

- Codex: `~/.agents/skills/reader-first/`
- Claude Code: `~/.claude/skills/reader-first/`

Use `--target codex` or `--target claude` for one environment. To share it inside a project:

```sh
python3 install.py --target both --scope project --project /path/to/project
```

The project locations are `.agents/skills/reader-first/` and `.claude/skills/reader-first/`. Commit the installed directory if you want teammates to receive it. Installation does not create context documents or change project instructions. A different existing installation is preserved unless you pass `--update`; that option backs it up before replacing it. Backups go in a `reader-first-backups` directory beside the `skills` directory, and the installer prints the exact path. Identical installs are a no-op. A custom final directory is supported with `--destination /path/to/skills/reader-first`.

Manual installation also works: copy **the entire** `skills/reader-first` directory into either environment's skills directory. No symlinks, other skills, API key, Wordflows account, model pin, or network service is required.

These are local agent installs. Web chats and cloud environments need their own supported upload/plugin mechanism. Check the current [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skill documentation](https://code.claude.com/docs/en/skills) if your environment uses a different layout. If the skill does not appear after installation, start a new session.

## Use

In Codex:

```text
$reader-first init
$reader-first audit the copy on our homepage
$reader-first rewrite this hero for independent teachers
$reader-first write an empty state for the worksheet list
$reader-first distill this onboarding message to 120 characters
$reader-first adapt this page for developer buyers
$reader-first decringe this draft while keeping its meaning
```

In Claude Code, use `/reader-first` with the same arguments. These are modes of one skill, not seven separately installed commands. You can also request copywriting or UX edits in natural language; automatic selection depends on the host agent.

For a quick edit, paste the text and explain the reader and relevant behavior. Setup is optional. `audit` reports findings without changing files; `write` and `rewrite` produce or edit the requested copy. None of the modes authorizes publishing or changing product behavior.

## Teach it your project

`init` uses what your agent can establish from the conversation and relevant project material to save reusable context. Unknowns remain marked; it should ask only for a fact that changes the result.

| File | Purpose |
| --- | --- |
| `AUDIENCE.md` | Reader situations, tasks, vocabulary, and evidence |
| `PRODUCT.md` | Verified capabilities, offer, limits, actions, and proof |
| `VOICE.md` | Optional approved voice examples and terminology |
| `.reader-first/briefs/<surface>.md` | Optional page/flow brief selecting an audience and next action |

Files may live at the selected app root or under `.reader-first/`. Existing equivalent records are reusable; `audience.md` is recognized too. Conflicting files are flagged, and the loader never silently inherits another app's context. If you already use Impeccable, keep its compatible `PRODUCT.md`; visual `DESIGN.md` stays separate.

Start with the [templates](skills/reader-first/assets/templates/) or the complete [fictional example](examples/lesson-draft/). The [context guide](skills/reader-first/references/context.md) explains ownership, evidence, and resolution.

## What it checks

- Technical implementation used where the reader needs a task or offer.
- Feature lists, interchangeable benefits, unclear positioning, and repeated sections.
- Unsupported outcomes, manufactured proof, invented customer psychology, and CTA mismatches.
- Internal UI terms, inaccurate states, invented error causes, and incorrect recovery or deletion promises.
- Canned contrasts, inflated significance, empty intensifiers, and repetitive AI cadence.

The [rule catalog](skills/reader-first/references/rules.md) includes exceptions. Developer audiences sometimes need technical detail; a verified trial can say “no card required”; an effective contrast or em dash can stay. Reader First reviews usefulness and truth, not authorship.

## Optional helpers

From the repository:

```sh
python3 skills/reader-first/scripts/check.py examples/lesson-draft/before.md --format json
python3 skills/reader-first/scripts/load_context.py --root examples/lesson-draft --brief BRIEF.md
```

The scanner finds candidates in plain text/Markdown. It does not evaluate the audience, verify claims, parse application source, or score AI probability. Zero candidates still requires contextual review. The [scanner contract](skills/reader-first/references/scanner.md) documents formats, masking, offsets, and exit codes. Installed helpers live inside the installed skill's `scripts/` directory.

## Development and release

```sh
python3 -B -m unittest discover -s tests -v
python3 scripts/package.py
```

The package command creates `dist/reader-first-0.1.0.zip` and refuses to overwrite an existing archive. Tests exercise candidate locations, Markdown masking, context ambiguity/isolation, install preservation, and portable packaging. [Behavioral evaluation cases](docs/evaluation.md) cover decisions a regex cannot test. [Research and product rationale](docs/research.md) explain the evidence and its limits.

Change substantive writing rules only when a real failure supports the change. New scanner patterns should be cues for contextual review, accompanied by a false-positive example. Preserve stable rule IDs. Contribution guidance is in [CONTRIBUTING.md](CONTRIBUTING.md).

## License and inspiration

MIT, copyright Lucas Weaver. The installed skill includes the license so it can be redistributed on its own.

Inspired by [Impeccable](https://impeccable.style/)'s focused commands and reusable context, and by the decontaminate/decringe approach of scanning candidates followed by judgment. Reader First is an independent implementation with no runtime dependency on those skills. It makes no guarantee about conversion, detection avoidance, or flawless model behavior.
