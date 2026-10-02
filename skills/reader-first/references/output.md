# Output and findings

Scale to the request. Finished writing comes first for writing modes. Audit findings come first for audits. Do not report each checklist item as a finding.

A substantive finding contains:

- **Location and span:** file/line or visible surface/state; quote enough to locate it.
- **Rule and judgment:** stable rule ID, confirmed problem or verification needed.
- **Consequence:** the misunderstanding or misleading decision this reader could make.
- **Evidence:** product fact, audience evidence, observed handler/state, or stated uncertainty.
- **Repair:** ready wording supported by the evidence, or the exact fact that must be checked.

Priorities describe consequences, not scanner certainty: **high** for misleading claims/actions or material omissions; **medium** for unclear offer, task, or terminology; **low** for style or avoidable repetition. Use judgment; jargon can be high priority if it hides a charge or destructive action.

For a full audit, a compact table works: `Priority | Location | Rule | Problem/evidence | Repair`. Keep overlapping rules in one finding. Separate unavailable verification from confirmed errors. A scanner candidate dismissed in context is not an unresolved defect.

For edits, identify changed files or supply the replacement copy, explain material meaning changes, and state actual validation. “Checked supplied copy against PRODUCT.md” is different from “verified in the live UI.” Do not imply deployment or conversion improvement from a wording pass.

Put assumptions and editorial notes outside publishable copy. Do not bury an unverified promise inside a draft with a vague final disclaimer. For a small edit, one replacement and a short qualification may be sufficient.
