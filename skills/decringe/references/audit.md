# Audit

Review the requested surface without changing files. A short replacement example is useful but is not an implemented fix.

Read the selected module guidance and [rules](rules.md). Establish audience, task, product facts, and action destination from context. If available, inspect the rendered text and relevant UI state; otherwise say the audit is based on supplied text. Scan substantial prose with `scripts/check.py`, then review meaning beyond the hits.

Prioritize issues that alter a reader's decision: false promises, misleading action labels, missing costs or restrictions, unclear offer, and unresolved error recovery. Style preferences follow those issues. Report only supported findings and distinguish a definite mismatch from a fact that needs verification.

Use [output](output.md). Give each issue a location, quoted span, rule ID, reader consequence, evidence, and a concrete repair or precise verification question. State coverage: supplied excerpt, whole page, inspected states, and unavailable paths. Avoid fake scores, AI percentages, and universal conversion predictions.

It is valid to find no material issues. Explain the scope checked and remaining verification gap without inventing nits.
