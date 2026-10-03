# Delegated review smoke run — 2026-10-03

The user identified a workflow regression: standalone Decringe had ported scanner cues and summarized guidance but did not explicitly require a separate model to receive all rules and return violations before correction. The repair is a bundled complete rulebook and an explicit lightweight-reviewer/report/correction/recheck protocol. Canonical module ownership and preserved counterexamples remain unchanged.

## Environment and scope

Codex desktop, requested subagent model `gpt-6-luna`, requested reasoning `medium`, fresh context (`fork_turns=none`). The spawn response exposed the task identity but no independently verifiable actual-model metadata. One reviewer read the complete generated REVIEW_RULES.md, review/report instructions and the [synthetic inputs](../../examples/semantic-review/cases.json). The input did not include expected outcomes or the parent's diagnosis. No Wordflows or external model API was called by the review protocol. Reviewer tasks were read-only and did not write product files.

The parent manually orchestrated the protocol while developing it. This tests the reviewer handoff and outputs, not automatic skill selection or every host's model-selection tool. Corrections reused the reviewer. Rechecking used exact corrected snapshots and original context; there were two semantic review rounds, with a correction task between them.

## Observed decisions

| Case | Initial report | Correction / recheck | Parent assessment |
| --- | --- | --- | --- |
| Article: paraphrased invented crowd and hollow “transformed mindset” payoff | STYLE-02 violation despite zero scanner candidates; missing substantive point identified | Reviewer declined to invent replacement advice. Article remained pending and was excluded from passing rechecks. | Semantic detection and conservative handling observed. No completed article claimed. |
| Developer CDC/encryption copy | No violations; preserved PostgreSQL logical replication, at-least-once delivery and intentional concrete encryption contrast despite scanner cues | Original text retained; recheck passed | Preservation case observed. |
| UI completion/save/archive strings | UX-03 caught “Everything is ready” despite no cue for that span; UX-04 rejected invented network cause/data safety; UX-02 identified delete/archive mismatch | “The worksheet item is complete. Export is still processing.” / “Couldn't save. Try again.” / “Archive project”; recheck passed | Truthful state/action repairs observed. |
| Teacher offer | COPY-01 implementation-led headline and COPY-05 unsupported accuracy/time savings; trial conditions retained | Draft workflow and required teacher review replaced claims; 14-day/card/$12/cancellation/five-draft terms retained; recheck passed | Supported copy repair and material-condition preservation observed. |

The first teacher report also duplicated the empty “seamless” adjective as a separate STYLE-03 finding even though the COPY-01 repair resolved it. The parent consolidated it before correction, as the protocol requires. A concrete overlap example was added to the review prompt; its general effectiveness is not established by this run.

## Limits

These are observed reviewer decisions on four synthetic cases, not a benchmark. No comparison with Wordflows' `gpt-5.4-mini-2026-03-17`, no Claude Code execution, no API model call, no measured token/cost savings, no full skill-autoselection test, and no reader/conversion evaluation was performed. Three supported revised cases received passing reports; the article still needed author context. Broader evaluation remains pending.
