---
name: decontaminate
description: Compatibility alias for an explicit decontaminate request. Forward the task to the sibling decringe skill; this alias has no independent writing rules.
disable-model-invocation: true
---

# Decontaminate compatibility alias

For an explicit invocation or a workflow that explicitly requires decontaminate, load `../decringe/SKILL.md` relative to this installed folder. Pass through the user's text, operation and context unchanged. Bare decontamination uses the core; requested SaaS or UI work selects the appropriate module. Follow Decringe once; do not run a second cleanup workflow here.

This alias depends on a sibling `decringe` install. The migration installer supplies both. If that sibling is missing, report the missing canonical skill rather than inventing fallback rules. This file owns no rule catalog or scanner. Existing semantic API/voice flags are not implemented by the offline helper; contextual judgment happens in the host agent.
