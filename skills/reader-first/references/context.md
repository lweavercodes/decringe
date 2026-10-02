# Reusable context

Context should change a writing decision. Keep it small enough to read and specific enough to resolve a tradeoff.

| Record | Owns | Does not establish |
| --- | --- | --- |
| `AUDIENCE.md` | Reader situations, tasks, vocabulary, decision criteria, evidence and uncertainty | Product capabilities or invented psychological profiles |
| `PRODUCT.md` | Current capabilities, offer, limitations, action outcomes, facts and proof sources | Customer demand or a guaranteed result |
| `VOICE.md` (optional) | Tone, approved examples, terminology and purposeful exceptions | Permission to exaggerate |
| `BRIEF.md` (optional, per surface) | Selected audience, page/flow objective, entry context, CTA destination, constraints | A new global positioning strategy |

Use equivalent existing documents such as Impeccable's `PRODUCT.md` rather than creating a competing product truth. `DESIGN.md` can supply visual constraints, but it is not required and does not substitute for knowing the audience. Respect any explicit ownership/location policy the project already uses.

## Resolve scope

1. Identify the target app or project from the user's files and request. In a monorepo, use the app root, not a sibling or the shell's arbitrary current directory.
2. Prefer explicit context supplied or named by the user. Within one chosen project, discover each record at the root or `.reader-first/`. Names are case-insensitive, so an existing `audience.md` works.
3. If both locations or case variants provide the same record, report ambiguity and inspect them. Select the authoritative one using project instructions or the user's context; do not merge contradictory records silently. Different record types may live in different supported locations within the same project.
4. Do not walk parent projects for fallback. Load shared context only when the project or user explicitly identifies it. This prevents one app's audience becoming another app's reader.
5. A surface brief is loaded only when selected by the task. Suggested home: `.reader-first/briefs/<surface>.md`. Reuse an existing surface record if it covers the same decisions.

The optional `scripts/load_context.py` implements step 2 and flags ambiguity. It reports record paths, not file contents. It rejects auto-discovered symlinks outside the chosen project; an explicitly supplied brief may live elsewhere. This prevents accidental cross-project context, not all possible access to sensitive files. Never use context discovery to search credentials.

## Evidence and conflict

Label knowledge as **confirmed**, **observed**, **hypothesis**, or **unknown**. Give a source and verification date when useful, especially for prices, availability, measurements, and quotations. These labels communicate provenance; they are not certifications.

An existing marketing sentence is not proof of its own claim. A customer quote describes that person's experience, not the entire market. A screenshot shows one UI state, not every error path. A test establishes its tested scope, not all deployment behavior.

Current user instructions control the task. If product records conflict with observed behavior, flag the mismatch and avoid promising the disputed behavior. Do not silently overwrite records during a copy edit. Ask only for the material fact needed, or provide useful conservative copy pending verification. Do not remove user-approved promises merely because you cannot independently browse their private evidence; identify the verification limit.

## Keep context maintainable

`init` writes confirmed context and explicitly marked hypotheses. Later commands consume it; they do not continually append preferences inferred from their own output. When updating context is requested, change the specific fact and its source, avoiding transcripts and repeated slogans. Redact personal/customer details before saving examples in an open repository.
