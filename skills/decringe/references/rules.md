# Rule ownership index

Each substantive rule has one owner. The detailed rule and its exceptions live only in that module; scanner cues live once in `patterns.json`. Shared constraints apply to all edits and do not create a separate findings pass.

| Owner | Rules | Canonical guidance |
| --- | --- | --- |
| Core | STYLE-01 through STYLE-08 | [core](core.md) |
| SaaS copy | COPY-01 through COPY-09 | [saas-copy](saas-copy.md) |
| UI | UX-01 through UX-07 | [ui](ui.md) |

## Boundary cases

- Empty language such as “effortlessly revolutionize” → core. A product's capabilities still fail to explain why it fits the reader → SaaS.
- Stack/pipeline dominates a teacher-facing hero → SaaS COPY-01. Internal enum/exception obscures a dashboard object or state → UI UX-01.
- Unmeasured savings or fabricated testimonial → SaaS COPY-05/06. Unsupported “your work is safe” or “we're investigating” → UI UX-04.
- A button says trial but requests a demo → UI UX-02. A page omits the trial's card requirement or price transition → SaaS COPY-07. A transactional form hides a charge before submission → UI UX-06.
- Repeated slogan fragments → core STYLE-04. Page sections fail to advance the buyer's decision → SaaS COPY-09. One duplicated sentence may have both symptoms: report one finding with the substantive owner and one repair.

## Mixed surfaces

A landing page is not all SaaS text. Map its marketing narrative to SaaS, controls/forms to UI, and apply core everywhere. A pricing-page CTA and its adjacent offer terms may need both modules across different spans; do not make competing edits to the same label.

Scanner profiles load only selected owners plus core. If the task is mixed, select `saas-copy+ui` and use span context to decide the owner of each resulting issue. Multiple candidates or contributing rule IDs do not require multiple findings. Candidate counts are not a measure of writing quality, authorship or conversion.
