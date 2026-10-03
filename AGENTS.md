# Maintaining Decringe

This repository is the editable source for the Decringe skill. Installed user/project skill directories are copies; make source changes here, validate, then refresh the requested installations with `python3 install.py --target both --update` or the appropriate single target.

Read `skills/decringe/references/maintenance.md` for the editable-file map and improvement loop. `skills/decringe/references/rules.md` is the ownership index. Core rules live in `core.md`, SaaS rules in `saas-copy.md`, UI rules in `ui.md`, and shared constraints in `shared.md` in the same reference directory. Do not maintain independent duplicate catalogs or give a rule multiple owners. `REVIEW_RULES.md` is the generated complete model-facing packet; rebuild it with `python3 skills/decringe/scripts/build_review_rules.py` after changes to the canonical modules/shared constraints. `references/reviewer.md` owns reviewer delegation/report/correction instructions.

Use the user's intended scope. Ordinary copy edits do not authorize changing the skill. For authorized skill improvements, retain a minimal redacted repro and a preservation counterexample using `skills/decringe/assets/templates/IMPROVEMENT_CASE.md`; fix the demonstrated cause rather than inventing global bans. Follow the bounded evaluation loop and report unrun model evaluations honestly.

Keep helpers Python 3.9+ and standard-library-only. Preserve read-only scanners/loaders, core inheritance, Unicode locations, context isolation, install backups and portable relative resources. Run `python3 -B -m unittest discover -s tests -v` after helper/resource/packaging changes. Behavioral cases in `docs/evaluation.md` require actual agent observations; helper tests do not prove copy quality or conversion.

Use conventional commits. Preserve unrelated changes. Keep `.decringe-source.json` local and out of commits/packages. Do not publish, push, create releases or message others merely because this file describes a workflow; follow the user's existing authorization.
