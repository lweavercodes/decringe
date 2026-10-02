# Failure patterns

These rules support judgment. Scanner-supported rules also have a `candidate` entry in `patterns.json`. Other rules require reading meaning, context, or behavior. Rule IDs remain stable so findings and evaluations can refer to them.

## Copywriting

| ID | Look for | Decision and repair | Keep when |
| --- | --- | --- | --- |
| COPY-01 | Implementation substituted for customer value | A stack, schema, or pipeline dominates text for readers who buy a different task. Translate to a supported capability and reader task, or move detail to evaluation material. | The audience needs the mechanism to evaluate compatibility, constraints, or operation. |
| COPY-02 | Features with no relevance | A list leaves the reader unable to tell what they can do. Connect features to an evidenced task; clear feature descriptions beat invented benefits. | A feature/compatibility table is the information the reader needs. |
| COPY-03 | Unrecognizable offer | Grand language obscures what is sold, for whom, or when it helps. Add a concrete task/category where the page needs it. | The surrounding context already establishes the offer; an expressive headline can be useful. |
| COPY-04 | Interchangeable benefit claims | “Powerful,” “seamless,” or “transformative” stands in for substance. Use supported capability, example, constraint, or proof. | The term has a literal domain meaning or is substantiated and useful. |
| COPY-05 | Unsupported or expanded promises | Claims exceed evidence on accuracy, performance, security, automation, guarantees, or outcomes. Bound the claim to established facts and conditions. | Evidence supports the exact claim and scope, including required qualifiers. |
| COPY-06 | Invented proof or scarcity | Testimonials, counts, certifications, logos, deadlines, or availability are invented to fill a template. Remove or mark the component for sourcing outside public copy. | Authentic evidence is supplied with usable attribution and conditions. |
| COPY-07 | CTA/offer mismatch | Copy promises a different destination, cost, commitment, or access than the flow provides. Match the actual next step and place key conditions nearby. | A generic label is unambiguous from its immediate context. |
| COPY-08 | Fabricated customer psychology | Assumed shame, fear, motives, or quotes are presented as research. Use observed situations and authentic language; label untested assumptions. | The chosen voice is intentional and the premise has evidence; do not universalize one interview. |
| COPY-09 | Repeated copy with no information gain | Sections repeat a generic promise or bury a necessary condition. Cut repetition or use the space to resolve a real decision. | Repetition aids comprehension, emphasis, or deliberate campaign voice. |

## UX writing

| ID | Look for | Decision and repair | Keep when |
| --- | --- | --- | --- |
| UX-01 | Internal terminology leaks | Storage names, enums, technical exceptions, or inconsistent labels replace the visible user object. Use the established interface vocabulary. | This is a developer tool and the exact technical term helps the task. |
| UX-02 | Label promises wrong action | Button wording obscures the handler's consequence or level of commitment. Name the actual action; inspect the route/state if possible. | “Continue” or “Done” is clear in context and true. |
| UX-03 | State is inaccurate | Empty vs loading, upload vs processing, queued vs completed, partial vs full success. Describe the observed state and available next step. | The state distinction does not affect understanding or action. |
| UX-04 | Error invents cause or recovery | Message blames connection/user, promises support, data safety, or retry without evidence. Say what is known and offer an available action. | The system detects that cause and the recovery path exists. |
| UX-05 | Consequence or recoverability is wrong | Deletion, archive, sharing, charges, and undo claims conflict with behavior. Use verified scope and consequence; flag unknown retention/recovery. | The claim has been verified for that action and item type. |
| UX-06 | Important conditions arrive too late | Cost, permissions, input requirements, or visibility are missing at the decision. Put the relevant fact before commitment. | The fact is already explicit and accessible where needed. |
| UX-07 | Text breaks functional or accessible meaning | Lost placeholders/plurals, inconsistent terms, icon-only ambiguity, positional instructions. Preserve functional contracts and task meaning. | The surrounding UI resolves the context and the accessible name is present. |

## Prose

| ID | Look for | Decision and repair | Keep when |
| --- | --- | --- | --- |
| STYLE-01 | Inflated significance | “Pivotal,” “testament,” or “revolutionary” inflates an ordinary fact. State the concrete importance if supported; otherwise remove. | The magnitude is meaningful, evidenced, and appropriate to the voice. |
| STYLE-02 | Canned rhetorical contrast | Repeated “not just X, but Y” or slogan fragments substitute for an actual distinction. Say the useful difference directly. | A genuine comparison clarifies the reader's choice or is purposeful rhetoric. |
| STYLE-03 | Empty intensifiers and praise | “Incredibly,” “truly,” “effortlessly,” “best-in-class” adds tone without information. Replace with substance or remove. | An authentic quote or intended voice warrants it, without misleading claims. |
| STYLE-04 | Synthetic cadence or redundant tail | Repeated identical lists, fragments, soft conclusions, or “in today's fast-paced world” fills space. Vary naturally or cut padding. | The pattern carries content, aids scanning, or establishes deliberate rhythm. |

## Decision examples

- “Webhook payload includes a retry count.” Keep for integration docs or developer evaluation; it is not evidence of leakage alone.
- “Your organization has been hydrated.” For a teacher's project UI, use the visible object and verified result. Do not rename backend entities.
- “Generate a worksheet draft from your notes.” Supported by the fictional example product. “Never plan a lesson again.” Unsupported expansion (COPY-05).
- “No card required.” Keep when the actual trial supports it; verify when unknown. A scanner cannot know the flow (COPY-07).
- “We couldn't save your changes.” Appropriate for a failed save. Add “Try again” only if retry is available, and “your draft is safe” only if retention is verified (UX-04).
- “Delete project permanently.” Requires verified permanent deletion. Do not repair unknown behavior by guessing that it archives (UX-05).
- “It's not just encrypted in transit; it's encrypted at rest too.” A meaningful technical distinction can survive STYLE-02.

Treat this catalog as hypotheses to inspect, not a taxonomy of everything written by AI. The same failures occur in human copy. Do not claim these patterns measure model quality or prove authorship.
