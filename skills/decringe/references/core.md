# Core decontamination

This module always runs. It owns AI-typical language and rhetorical moves; it does not develop positioning or infer product behavior. Apply [shared constraints](shared.md) throughout.

## One language rule set

| ID | Candidate | Judgment and repair | Preserve when |
| --- | --- | --- | --- |
| STYLE-01 | Inflated significance: pivotal, revolutionary, “this matters,” “testament” | Replace the announcement with a supported consequence or remove empty importance. | Literal or evidenced significance helps this reader. |
| STYLE-02 | Canned contrasts and theatrical pivots: not-X-but-Y, “That sounds small. It isn't,” staged concession/correction | State the real distinction directly; remove a hollow uplift or invented mistaken crowd. | The contrast is concrete, purposeful and delivered by the surrounding text. |
| STYLE-03 | Empty praise, intensifiers and fashionable vocabulary: seamless, powerful, delve, leverage | Keep the actual capability or specific fact; remove decoration when no substance is lost. | Literal domain meaning, deliberate voice or an authentic quotation warrants it. |
| STYLE-04 | Stock transitions, redundant tails, repetitive fragments/lists, self-answered questions, punchline authority tags | Use the actual relationship or a normal sentence; cut repetition with no information gain. | Scanning, rhythm, emphasis or literal reference makes the form useful. |
| STYLE-05 | Performed honesty or intimacy: “let's be real,” “here's what nobody tells you” | Begin with the actual point rather than manufactured candor. | It is an authentic quotation or intentional voice with a real purpose. |
| STYLE-06 | Empty promise framing: “by the end of this guide...” | Start with useful substance when the introduction only promises it. | A learning objective or navigation contract helps the reader. |
| STYLE-07 | Puffed-up copulas: “serves as,” “functions as” | Use a plain verb when meaning is unchanged. | A literal role/function distinction needs the phrasing. |
| STYLE-08 | Repeated theatrical em-dash pauses | Inspect cadence and vary sentence structure if it feels mechanical. | Parenthetical meaning or purposeful voice needs the dashes. No punctuation ban. |

Exact scanner candidates live once in `patterns.json`, with module `core`; exact patterns are optional reference material, not automatic violations. The richer patterns preserve the original decringe catalog's lexical, phrase, rhetorical and cadence coverage. Do not substitute one flagged synonym for another while keeping the hollow move.

## Specificity without fabrication

Prefer the most concrete detail actually available: vague category → specific issue → concrete instance → lived detail. “The company had cashflow issues” can become “missed payroll twice” only if that fact is established. A one-word button need not sound like a personal story. A low-detail draft is not permission to invent metrics, founder experiences or customer voices.

Read the whole passage, not just hit locations. Paraphrases can reproduce the same rhetorical move without matching a pattern. Conversely, a developer's “ecosystem,” a pipe's “seamless,” or a real comparison can be correct. Preserve the author's voice rather than making everything casually minimalist.

## Core workflow

Scan substantial drafts, judge each candidate, and reread unflagged prose for the underlying moves. For a tiny label, a direct contextual check is enough. Revise supported problems within the requested scope. Reread the final deliverable and check that stylistic fixes have not changed facts or removed useful conditions. Use the explicit semantic-review and correction protocol in [reviewer](reviewer.md); a clean scanner result never completes the contextual pass.

## Complete legacy tell cards

These are the 21 ported legacy tells, grouped under the stable STYLE owners above. A card's `tell_id` identifies a specific move; report its STYLE rule as the canonical owner. Interpret the move in context, including paraphrases, rather than treating examples as regex instructions. Every card inherits the preservation column above and shared constraints: retain literal meaning, audience-needed terminology, authentic quotations and intentional effective voice. Several cues on one span may describe one violation; report one repair.

### STYLE-01 / `that-x-matters` — That X matters

**Detect:** Generic significance tagging detected.

**Example/cue:** And that is why this matters.

**Repair:** Show the consequence directly instead of saying that it matters.

**Preservation example:** This matters because the refund window closes in 24 hours.

### STYLE-01 / `why-that-matters` — Why that matters

**Detect:** Generic significance explainer phrase detected.

**Example/cue:** Why that matters: this changes everything.

**Repair:** Name the concrete consequence instead of announcing a meaning section.

### STYLE-03 / `high-frequency-ai-words` — High-frequency AI words

**Detect:** High-frequency AI vocabulary detected.

**Examples/cues:** delve; delves; delving; pivotal; crucial; foster; fosters; fostering; meticulous; meticulously; underscore; underscores; underscoring; showcase; showcases; showcasing; vibrant; testament; realm; groundbreaking; unprecedented; elevate; elevates; elevating; harness; harnesses; harnessing; empower; empowers; empowering; streamline; streamlines; streamlining; resonate; resonates; resonating; garner; garners; garnering; fundamentally; remarkably; notably; synergy; ecosystem; paradigm.

**Repair:** Replace with plain, specific alternatives.

### STYLE-04 / `generic-transitions` — Generic transitions

**Detect:** Generic AI transition detected.

**Examples/cues:** furthermore; moreover; additionally; in addition; in conclusion; it's worth noting; it is worth noting; it should be noted; it's important to remember; it is important to remember; in today's world; in today's fast-paced; in the ever-evolving; when it comes to.

**Repair:** Cut the transition or use a voice-specific bridge.

**Preservation example:** When it comes to refunds, email us within 30 days.

### STYLE-07 / `copula-avoidance` — Copula avoidance

**Detect:** AI formalism detected: replacing plain 'is/are/has' with a puffed-up substitute.

**Examples/cues:** serves as; stands as; acts as; functions as; works as; operates as.

**Repair:** Use 'is', 'are', or 'has' where possible.

### STYLE-01 / `significance-inflation` — Significance inflation

**Detect:** Significance inflation detected.

**Examples/cues:** plays a significant role; plays a crucial role; plays a pivotal role; represents a significant; represents a fundamental; marks a pivotal; marks a significant; setting the stage for; indelible mark; the implications cannot be overstated; cannot be overstated; at the forefront of; a testament to; underscores the importance; highlights the importance.

**Repair:** State what the thing actually changes or causes.

### STYLE-05 / `false-intimacy` — False intimacy

**Detect:** Manufactured vulnerability or false candor detected.

**Examples/cues:** i'll be honest with you; i'll be honest,; let's be real; here's what most people won't tell you; here's what nobody tells you; here's the truth; unpopular opinion:; controversial opinion:; i know this might be controversial.

**Repair:** Delete the performance of honesty and start with the actual point.

### STYLE-06 / `promise-framing` — Promise framing

**Detect:** Generic promise framing detected.

**Examples/cues:** by the end of this section; by the end of this article; by the end of this guide; by the end of this comparison; by the end of this post; what you'll learn; what you will learn; what this guide delivers; what you'll be able to do; what you will be able to do; in this section, you'll; in this section, you will.

**Repair:** Start with the useful claim, constraint, or decision rule directly.

### STYLE-04 / `tricolon-negation` — Not X. Not Y. Just Z.

**Detect:** Three-beat negation pattern detected.

**Example/cue:** Not a tool. Not a platform. Just results.

**Repair:** Use a two-beat contrast or a direct claim.

### STYLE-02 / `not-x-but-y-reframe` — Not X but Y reframe

**Detect:** Generic not-X-but-Y uplift reframe detected.

**Example/cue:** This is not about writing faster. It is about unlocking your potential.

**Repair:** Replace with a direct positive claim or scoped contrast.

**Preserve:** Apply the hollow-vs-earned test. Flag only when Y is vague significance — a category like 'mindset', 'philosophy', 'systems', 'the process' — that hides the absence of a point. Keep the contrast when Y is concrete (an instance, number, or mechanism — Level 3+ on the specificity ladder) AND the surrounding text delivers it. The shape alone is not the tell; a hollow Y is. When in doubt and Y is concrete, do not flag.

**Preservation example:** Most people meal prep Sunday. The most consistent clients I know prep nothing and cook one thing daily.

**Preservation example:** It's not a 10% lift. It's 3x once you paste the prior chat into the system prompt.

### STYLE-02 / `generic-not-x-it-is-y-reframe` — Generic X is not Y. It is Z.

**Detect:** Generic correction-to-uplift structure detected.

**Example/cue:** Success is not a destination. It is a journey.

**Repair:** Keep the contrast concrete and avoid the canned second-sentence pivot.

**Preserve:** Apply the hollow-vs-earned test. Flag only when the second clause swaps one abstraction for a vaguer one ('not a destination, a journey'). Keep it when the second clause lands a concrete, deliverable specific (Level 3+ on the specificity ladder) that the body pays off. When in doubt and the payoff is concrete, do not flag.

**Preservation example:** The bottleneck wasn't headcount. It was the two-week approval queue between design and ship.

### STYLE-02 / `minimization-reversal` — That sounds small. It isn't.

**Detect:** Minimization reversal cadence detected.

**Example/cue:** That sounds small. It isn't.

**Repair:** State the consequence directly without the small-but-not-small beat.

### STYLE-02 / `performed-concession-pivot` — Performed concession pivot

**Detect:** Invented objection followed by a one-word concession detected.

**Example/cue:** You might think this is overkill. Fair. But hear me out.

**Repair:** Remove the staged objection and state the stronger evidence directly.

### STYLE-02 / `standalone-concession-pivot` — Sure. But.

**Detect:** Standalone concession pivot detected.

**Example/cue:** Sure. But this changes everything.

**Repair:** Merge into a direct scoped contrast.

### STYLE-02 / `misconception-correction` — The mistake people make is thinking X. It isn't.

**Detect:** Misconception-correction template detected.

**Example/cue:** The mistake people make is thinking it is about talent. It isn't.

**Repair:** Make the observation directly without inventing a generic mistaken crowd.

### STYLE-04 / `self-answered-question` — Self-answered question fragment

**Detect:** Dramatic question fragment answered immediately.

**Example/cue:** The result? Better work.

**Repair:** Convert it to a declarative sentence.

### STYLE-04 / `synthetic-specificity-bridges` — Synthetic specificity bridges

**Detect:** Synthetic specificity bridge detected.

**Examples/cues:** more concretely,; here's what i mean; and here's the part most people miss; but here's the truth.

**Repair:** Move directly into the specific example or claim.

### STYLE-04 / `thats-the-authority-tag` — That's the X.

**Detect:** Punchline authority tag detected.

**Example/cue:** Ship it, then fix it. That's the move.

**Repair:** State the idea directly instead of ending with the canned authority beat.

**Preservation example:** That's the third option on the list.

### STYLE-04 / `known-punchline-authority-tags` — Known punchline authority tags

**Detect:** Canned punchline authority tag detected.

**Examples/cues:** that's the job.; that's the point.; that's the move.; wrong diagnosis..

**Repair:** Remove the authority beat and keep the underlying idea.

### STYLE-04 / `rhetorical-question-opener` — Have you ever opener

**Detect:** Well-worn rhetorical opener detected.

**Example/cue:** Have you ever wondered why your copy sounds robotic? Also inspect paraphrases such as Ever wondered, Picture this, and Imagine a world where.

**Repair:** State the observation directly.

### STYLE-08 / `em-dash-overuse` — Em-dash overuse

**Detect:** Multiple theatrical em-dash pauses detected.

**Example/cue:** It is fast — really fast — and simple — almost too simple. Repeated theatrical pauses need a cadence check, not a punctuation ban.

**Repair:** Use commas or semicolons, and reserve em-dashes for real parenthetical asides.
