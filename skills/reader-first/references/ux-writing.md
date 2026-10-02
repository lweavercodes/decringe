# UX writing decisions

UI text is part of product behavior. Check the state, the action, and its consequence before polishing the sentence.

## Speak in the reader's model

Use the term the reader uses for the object. A backend `organization` may be a visible “project.” Keep that mapping consistent without renaming the data model. Domain terms that users rely on should stay; unexplained internal enum values and exception messages rarely belong in consumer text.

Button and link labels should identify the action in context. “Save draft,” “Request access,” and “Archive project” make different promises. “Continue” can work when the next step is already clear. Do not force a long descriptive label into every button.

## Write the actual state

Distinguish empty, loading, pending, success, partial success, validation error, permission denial, and unexpected failure. “No results” is inaccurate while a query is still loading. A successful upload is not a completed import. A queued job is not a finished document. Say what happened at the scope the system knows.

Errors should explain what is known and provide an available recovery action. Do not invent a cause (“your connection dropped”), staffed response (“we're investigating”), preserved data (“your work is safe”), or retry control. When cause is unknown, a neutral task-specific message is appropriate. Avoid exposed stack traces and blame; relevant error IDs can help support if that workflow exists.

For destructive or consequential actions, describe the affected object and material consequence. Verify whether recovery, undo, cancellation, and retention actually exist. Do not relabel deletion as removal or promise permanence when the item is archived. A lack of verified recovery is an unresolved fact, not permission to assert “cannot be undone.”

## Reduce uncertainty at the right moment

Explain costs, requirements, sharing visibility, and permissions where they change the user's decision. Put instructions before the user makes the mistake. Avoid ornamental reassurance or legal-sounding claims without a product fact behind them.

Empty states should identify the state and an available next step, if one exists. Loading messages should reflect observable progress without fake durations or completion claims. Onboarding should teach the immediate task rather than repeat landing-page slogans.

## Preserve functional text

Check interpolation and plural forms, screen reader names, focus context, space limits, and terminology in surrounding screens. A visible icon still needs an appropriate accessible name. Do not use color, position, or a joke as the only instruction. Avoid claiming accessibility compliance from a wording review alone.

When behavior is unavailable, provide conditional wording with the missing fact outside the publishable text. Verify the relevant path or report the limit; do not silently repair behavior through copy.
