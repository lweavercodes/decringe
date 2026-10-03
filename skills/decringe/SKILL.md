---
name: decringe
description: Remove AI tells from authored prose and review SaaS marketing or UI text with focused modules. Use for decontamination, robotic rhetoric, vague product copy, implementation jargon, misleading claims, or confusing labels and states.
---

# Decringe

One skill with an always-applied decontamination core and optional `saas-copy` and `ui` modules. Restore useful human writing and the author's intended voice. Each module owns its own checks; combine them into one review and one coherent edit.

Apply to authored deliverables: landing pages, emails, articles, scripts, social posts, and interface text. Do not automatically polish ordinary agent replies, research analysis, technical explanations, code, or configuration. Developer-facing marketing and UI still qualify; preserve technical terms those readers need.

## Route the request

Apply [shared constraints](references/shared.md) on every invocation. The semantic reviewer receives the complete [reviewer rulebook](references/REVIEW_RULES.md), including core. Read [core](references/core.md) directly for authoring guidance or self-review when needed. Select the expertise separately from the operation:

| Module | Trigger | Additional guidance |
| --- | --- | --- |
| `core` (default) | General prose cleanup; no specialist task requested | No specialist reference |
| `saas-copy` | Write/review SaaS marketing, positioning, product pages, pricing or offer explanations | [saas-copy](references/saas-copy.md) |
| `ui` | Write/review controls, labels, forms, navigation, onboarding or interface states | [ui](references/ui.md) |
| `saas-copy+ui` | A full marketing surface with forms/controls, or an explicitly mixed request | Both module references, scoped by text purpose |

Explicit module selection defines scope. Otherwise infer from the requested work: generic “decringe this” means core; a homepage copy rewrite implies SaaS guidance; a button edit implies UI guidance. For a landing-page audit, route marketing sections to SaaS and forms/controls to UI. Do not apply every module to every sentence.

Choose an operation independently: [audit](references/audit.md), [write](references/write.md), [rewrite](references/rewrite.md), [distill](references/distill.md), or [adapt](references/adapt.md). A review is read-only; a fix authorizes the scoped copy edit. Bare `decringe <draft>` means core rewrite. An omitted operation is inferred from the request. [Init](references/init.md) records context and does not rewrite live copy unless requested.

When the user asks to improve Decringe itself, use `improve` and read [maintenance](references/maintenance.md). This updates the skill's rules or resources; it is separate from improving a customer's copy.

Examples of arguments to this one skill (not separate native commands):

```text
decringe <draft>
decringe saas-copy audit <page>
decringe saas-copy rewrite <hero>
decringe ui rewrite <component>
decringe saas-copy+ui audit <landing-page>
decringe init
decringe improve <observed-failure>
```

## Establish context

Read [context](references/context.md) when loading or recording reusable context. Use audience, facts and voice already supplied. `AUDIENCE.md` describes readers; `PRODUCT.md` establishes behavior and offers; optional `VOICE.md` gives approved examples; a selected surface brief defines this task. Equivalent existing records count. No mandatory setup interview for a narrow edit.

The optional read-only loader reports named records within one selected app:

```sh
python3 <skill-dir>/scripts/load_context.py --root <project-root> --brief <brief-path>
```

Resolve `<skill-dir>` from this loaded SKILL.md; omit absent brief arguments. Inspect ambiguities, do not silently mix applications. Ask only when an unknown fact materially changes the result; otherwise proceed conservatively and state the assumption outside the copy.

## Required semantic review, then correction

Follow [reviewer](references/reviewer.md) for every authored draft being audited or delivered. **Use a lightweight, explicitly selected subagent for the semantic review when available and permitted.** Send the complete [REVIEW_RULES.md](references/REVIEW_RULES.md), exact draft, selected modules, audience/product/voice context and optional scanner results. The reviewer returns violations with rule IDs, verbatim snippets, reasons and supported repairs; it reviews paraphrased moves and unflagged text too. A Python scan is an auxiliary check, never a replacement for this model review.

1. Establish the draft and constraints; map marketing text to SaaS and controls/states to UI. Core applies throughout.
2. Scan substantial visible prose with `scripts/check.py` when Python is available, using the selected profile. See [scanner](references/scanner.md); extract visible strings from source rather than scanning identifiers as copy.
3. Delegate the explicit semantic review using the available host tool with a suitable lower-cost model. Select that model explicitly rather than silently inheriting Sol/Astra/Opus; see the host-aware selection and fallback in [reviewer](references/reviewer.md). Do not assume an API Mini model exists in a subscription's model list. In a constrained host, perform the same explicit rulebook review yourself and disclose the fallback; do not omit the semantic pass.
4. Wait for and validate the report: exact quotes, selected rule IDs, complete coverage, product truth and preservation constraints. Consolidate overlapping findings. For `audit`, report findings without editing.
5. For writing/editing operations, apply supported fixes coherently. Correct directly or send accepted findings to the same subagent for corrected copy; a separate editor is optional. The parent applies files and checks behavior, facts, qualifications and functional strings.
6. After material corrections, request a semantic recheck of the revised draft, reuse the reviewer where possible, and rescan substantial text. At most three semantic review rounds total; report unresolved issues. Final parent verification still applies.

Follow [output](references/output.md). Lead with finished copy or consequential findings; identify actual review method/model where known and verification limits. `init` records context and `improve` maintains the skill; neither requires reviewing this skill's instructional Markdown as customer prose.

## Workflow integration

Every invocation includes the core, including specialist work. Native content workflows should explicitly invoke Decringe at the authored-output boundary with the appropriate module; automatic skill selection alone is not enforcement. Use the same bundled semantic reviewer protocol and rulebook rather than retaining a second decontamination catalog. The optional legacy `decontaminate` alias forwards to this skill and owns no rules.

## Editable source and improvement

Canonical repository: [lweavercodes/decringe](https://github.com/lweavercodes/decringe). Editable skill Markdown lives in the repository's `skills/decringe/` directory. [rules.md](references/rules.md) indexes the single owner of each rule; edit [core.md](references/core.md), [saas-copy.md](references/saas-copy.md), or [ui.md](references/ui.md) for the actual decisions and exceptions. Shared guardrails live in [shared.md](references/shared.md). The complete model-facing [REVIEW_RULES.md](references/REVIEW_RULES.md) is generated from those canonical files; after edits, run `python3 skills/decringe/scripts/build_review_rules.py` from the repository root. Reviewer delegation/report/correction instructions live in [reviewer.md](references/reviewer.md).

For maintenance, check `.decringe-source.json` beside this installed SKILL.md. The installer records the source directory and whether it is a Git checkout. Treat that record as a location hint, verify the repository, and edit the intended source checkout before refreshing installed copies. Manual installs may lack the record; locate or clone the canonical repository or the user's chosen fork. Do not hardcode another user's local path.

Follow [maintenance](references/maintenance.md) for the complete editable-file map and bounded evidence → rule change → evaluation → regression check loop. Ordinary writing jobs do not authorize rewriting the skill or silently learning new global bans from their own output.
