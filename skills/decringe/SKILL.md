---
name: decringe
description: Remove AI tells from authored prose and review SaaS marketing or UI text with focused modules. Use for decontamination, robotic rhetoric, vague product copy, implementation jargon, misleading claims, or confusing labels and states.
---

# Decringe

One skill with an always-applied decontamination core and optional `saas-copy` and `ui` modules. Restore useful human writing and the author's intended voice. Each module owns its own checks; combine them into one review and one coherent edit.

Apply to authored deliverables: landing pages, emails, articles, scripts, social posts, and interface text. Do not automatically polish ordinary agent replies, research analysis, technical explanations, code, or configuration. Developer-facing marketing and UI still qualify; preserve technical terms those readers need.

## Route the request

Read [core](references/core.md) and [shared constraints](references/shared.md) on every invocation. Select the expertise separately from the operation:

| Module | Trigger | Additional guidance |
| --- | --- | --- |
| `core` (default) | General prose cleanup; no specialist task requested | No specialist reference |
| `saas-copy` | Write/review SaaS marketing, positioning, product pages, pricing or offer explanations | [saas-copy](references/saas-copy.md) |
| `ui` | Write/review controls, labels, forms, navigation, onboarding or interface states | [ui](references/ui.md) |
| `saas-copy+ui` | A full marketing surface with forms/controls, or an explicitly mixed request | Both module references, scoped by text purpose |

Explicit module selection defines scope. Otherwise infer from the requested work: generic “decringe this” means core; a homepage copy rewrite implies SaaS guidance; a button edit implies UI guidance. For a landing-page audit, route marketing sections to SaaS and forms/controls to UI. Do not apply every module to every sentence.

Choose an operation independently: [audit](references/audit.md), [write](references/write.md), [rewrite](references/rewrite.md), [distill](references/distill.md), or [adapt](references/adapt.md). A review is read-only; a fix authorizes the scoped copy edit. Bare `decringe <draft>` means core rewrite. An omitted operation is inferred from the request. [Init](references/init.md) records context and does not rewrite live copy unless requested.

Examples of arguments to this one skill (not separate native commands):

```text
decringe <draft>
decringe saas-copy audit <page>
decringe saas-copy rewrite <hero>
decringe ui rewrite <component>
decringe saas-copy+ui audit <landing-page>
decringe init
```

## Establish context

Read [context](references/context.md) when loading or recording reusable context. Use audience, facts and voice already supplied. `AUDIENCE.md` describes readers; `PRODUCT.md` establishes behavior and offers; optional `VOICE.md` gives approved examples; a selected surface brief defines this task. Equivalent existing records count. No mandatory setup interview for a narrow edit.

The optional read-only loader reports named records within one selected app:

```sh
python3 <skill-dir>/scripts/load_context.py --root <project-root> --brief <brief-path>
```

Resolve `<skill-dir>` from this loaded SKILL.md; omit absent brief arguments. Inspect ambiguities, do not silently mix applications. Ask only when an unknown fact materially changes the result; otherwise proceed conservatively and state the assumption outside the copy.

## Review once, edit coherently

1. Map each span to its task. Core checks language everywhere. SaaS checks offer/reader decisions. UI checks controls and interaction states, including on a marketing page.
2. Scan substantial visible text if Python is available, selecting the relevant profile:

   ```sh
   python3 <skill-dir>/scripts/check.py <copy.md> --profile saas-copy+ui --format json
   ```

   Default profile is `core`; every profile includes core patterns. Read [scanner](references/scanner.md) for limitations and exit codes. Scan extracted prose, not source identifiers as published copy.
3. Judge candidates and unflagged meaning using the selected references. Findings are hypotheses, not AI detection or a quality score. Useful words, contrasts, repetition and punctuation can stay. Zero hits still requires contextual review.
4. Use the rule's single owner. When overlapping candidates describe one problem, report one finding and one repair. Action-label correctness belongs to UI; offer conditions and buyer commitment belong to SaaS; generic rhetoric belongs to core. See [ownership index](references/rules.md).
5. Make one coherent edit for the authorized operation. Apply final core cleanup to any new wording, then compare facts, qualifications, voice and behavior with the original/context. Rescan substantial revisions once; repeat only for unresolved issues, at most three meaningful passes. Do not rewrite separately for each module or optimize for an empty scan.

Follow [output](references/output.md). Lead with finished copy or consequential findings, identify changed files versus suggestions, and state actual verification limits. Tiny edits need proportionate responses.

## Workflow integration

Every invocation includes the core, including specialist work. Native content workflows should explicitly invoke Decringe at the authored-output boundary with the appropriate module; automatic skill selection alone is not enforcement. Use this same bundled rule set rather than retaining a second decontamination catalog. The optional legacy `decontaminate` alias forwards to this skill and owns no rules.
