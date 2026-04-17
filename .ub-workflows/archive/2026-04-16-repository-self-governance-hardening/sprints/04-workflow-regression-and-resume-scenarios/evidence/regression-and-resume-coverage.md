# Sprint 04 Evidence

## Coverage Map

Sprint 04 extended `test_scaffold_initiative.py` with scenario-style coverage
for the corrected workflow lifecycle.

New or newly expanded protections:

1. `test_prepare_sprints_blocks_without_roadmap_approval`
   - protects roadmap approval gating before sprint-pack preparation
2. `test_resume_order_for_placeholder_sprint_falls_back_to_prd`
   - protects the original rich-roadmap but placeholder-only sprint failure mode
3. `test_resume_order_for_later_prepared_sprint_uses_prior_closeout_without_prd`
   - protects later-sprint session-reset resume order
4. `test_archive_blocks_without_archive_review_gate`
   - protects the final review pause before archive

Existing Sprint 03 protections that remain part of the same lifecycle baseline:

1. `test_prepare_sprints_renders_roadmap_metadata_into_sprint_prds`
2. `test_prepare_sprints_preserves_non_placeholder_sprint_docs`
3. `test_prepare_sprints_accepts_recorded_roadmap_approval_after_gate_advances`

## Original Failure Mode Regression

The concrete failure mode discovered in the live initiative was:

1. `roadmap.md` can be rich and fully planned
2. `init-sprints` can materialize sprint directories
3. the active sprint `sprint.md` can still be a placeholder shell
4. resume or execution then depends on reopening `prd.md` or chat context

The new regression coverage protects that behavior mechanically:

1. placeholder-only sprint PRDs now force resume order to include `prd.md`
2. prepared later sprints no longer require `prd.md` when roadmap, prior
   closeout, and sprint PRD are sufficient

## Session-Reset Resume Order

For a later prepared sprint, the protected minimal resume order is now:

1. `./roadmap.md`
2. the previous sprint `closeout.md`
3. the active or next sprint `sprint.md`
4. `./README.md`

`./prd.md` is included only when the sprint PRD is still missing or still
contains blocking placeholders.

## Archive Review Protection

Archive is now blocked unless `README.md` records one of:

1. `archive_ready: pass`
2. `initiative_complete: pass`

This keeps the final-audit review pause explicit instead of treating a complete
roadmap checklist as sufficient by itself.
