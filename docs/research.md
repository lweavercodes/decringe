# Research and product rationale

Research reviewed October 2, 2026; packaging and rule ownership updated October 3, 2026. This is a qualitative design rationale, not a representative survey, model comparison, or measured conversion study. Reddit posts are self-reports; several authors promote copywriting or audit products. Their commercial incentives and anecdotes are reasons to test the proposed rules, not proof that the rules improve sales.

## Complaints and counterexamples

| Primary discussion | Observation | Product response |
| --- | --- | --- |
| [EntrepreneurRideAlong: stop with AI on landing pages](https://www.reddit.com/r/EntrepreneurRideAlong/comments/1tumnrj/you_guys_gotta_stop_with_ai_on_landing_pages/) | Participants complain about confident, interchangeable copy and failures across UX/marketing/help text. One commenter recommends authentic customer material instead of letting the model invent substance. The thread also includes anecdotal performance claims we have not verified. | Separate audience evidence from product facts, review meaning after scanning, and route marketing and UX to different decision guides. COPY-03/04/08 and the UX rules. |
| [SaaS: a rewrite still sounded AI-generated](https://www.reddit.com/r/SaaS/comments/1tw1hmt/i_tried_to_rewrite_a_founders_copy_and_produced/) | The author says replacing a concrete feature description with a formulaic founder anecdote did not solve the problem. The post promotes a forthcoming solution. | Do not invent founder voice or a backstory. Preserve useful details and source voice examples. COPY-02/08, STYLE-02/04. |
| [SaaS: does AI-sounding copy make people bounce?](https://www.reddit.com/r/SaaS/comments/1uq7fvs/does_ai_sounding_landing_page_actually_make_you/) | A founder removed buzzwords but also replaced a numerical plan limit with vaguer use-case language. A commenter wanted the usage number retained to evaluate the offer. Another says positioning mattered more than AI authorship. | A decringe pass must preserve material limits and practical decision information. COPY-05/07; distill must not hide restrictions. |
| [Lovable: building a landing-page audit tool](https://www.reddit.com/r/lovable/comments/1q3su7r/im_a_marketer_who_cant_code_vibe_coding_helped_me/) | A promotional project post identifies vague headlines, pricing visibility, and hierarchy as repeat problems. A participant mentions button-copy feedback being useful after focusing on development. | Check offer and action together, rather than just tone. COPY-03/07/09 and UX-02/06. This supports a candidate checklist, not the poster's claimed error frequency. |
| [VibeCodingSaaS: who writes the landing-page copy?](https://www.reddit.com/r/VibeCodingSaaS/comments/1pll1mm/you_vibe_coded_your_saas_in_a_weekend_but_whos/) | A service promotion describes functioning apps paired with feature bullets and generic category wording. | Review the capability-to-task connection while allowing features where useful. COPY-02/03. Commercial framing limits how much weight this adds. |

The retrieved material supports the broader problem of generic, feature-heavy, or misleading copy. It does **not** establish how often agents copy internal identifiers or tech stacks into consumer landing pages, or that the newest models fail at a particular rate. Implementation leakage is a concrete failure described by the commissioning user and an inference worth testing. The scanner marks it as audience-dependent; it cannot prove that a technical term is wrong.

## What we borrow from Impeccable

[Impeccable's context documentation](https://impeccable.style/docs/context/) describes reusable product/design records and surface context. Its [public repository](https://github.com/pbakaus/impeccable) supplies focused design workflows. Decringe adopts the organizational idea: one discoverable skill, task-specific modes, compact shared context, and deeper guidance loaded when needed.

Our records focus on reader decisions: `AUDIENCE.md` holds evidence about readers, `PRODUCT.md` holds supported facts, optional `VOICE.md` captures approved examples, and a surface brief selects the task and action. Existing product records can be reused. No visual token system, browser hook, hosted service, or installed Impeccable dependency is needed. The content and scripts here were written for Decringe; no Impeccable source was copied.

## Extension beyond decringe

The existing decringe/decontaminate pattern suggests a useful sequence: deterministic candidate scan, contextual decision, scoped edit, and reread. Decringe adds a separate test of audience relevance and factual behavior. This lets it catch a plain but misleading “Done,” a fluent unverified savings claim, or an accurate internal term that the intended reader cannot use.

The product hypothesis is that reusable context and explicit decision rules reduce repeated repair work. Validation still requires observing real agent outputs and testing consequential copy with appropriate readers. No scanner score substitutes for that.

## Portability

Installation follows the current [Codex skill docs](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skill docs](https://code.claude.com/docs/en/skills): the same folder with `SKILL.md` and relative supporting files. Codex UI metadata is isolated in `agents/openai.yaml`; Claude does not need it. Commands are examples of a single skill's mode argument, not provider-specific extensions.

## Consolidation into Decringe v0.2

The initial package was called Reader First. The agreed product name is now Decringe. Its richer legacy decontamination patterns are consolidated into one core; `saas-copy` and `ui` add specialist decisions, not additional general cleanup catalogs. Each rule has one owner. Context and helper tests remain shared; the name change does not add evidence of conversion or cross-model effectiveness.
