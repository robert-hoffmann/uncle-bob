# Human User Guide

## Purpose

This is the quick-start version of the workflow.

Use `operation-guide.md` for the formal rules. Use this file when you want the
short human process.

## The Workflow

1. A human creates the initial PRD.
2. Run `python .agents/skills/ub-workflow/scripts/scaffold_initiative.py create --prd-source <path-to-prd>`.
3. Confirm `./prd.md` is complete and self-contained.
4. Generate the full `roadmap.md` from that PRD in one pass.
5. Review the roadmap with the agent's checklist.
6. If the roadmap is correct, explicitly approve it and mark `roadmap_ready: pass`.
7. Run `python .agents/skills/ub-workflow/scripts/scaffold_initiative.py init-sprints <initiative-root>`.
8. Stop and wait until the user explicitly asks to execute the active sprint.
9. Execute one sprint at a time.
10. After each sprint, stop for human review before moving to the next sprint.
11. End the roadmap with a final audit.
12. Stop for final human review before archive or other closure actions.
13. Ask whether any follow-up audits or refactors are wanted.
14. Write the retained note.

## Mental Model

1. `prd.md` explains the whole initiative.
2. `roadmap.md` is the durable post-plan artifact and the small live tracker.
3. Each sprint `sprint.md` is a standalone mini-PRD.
4. The helper bootstraps the operations root if `./.ub-workflows/` does not exist.
5. The helper uses the skill's internal templates, so you do not need to copy a local `initiative-template/` folder into the operations root.
6. Sprint folders are never created during the initial scaffold step.
7. Sprint initialization is scaffolding only; it does not start Sprint 01 automatically.
8. The workflow pauses after every sprint and after final audit so the human can review.

## Archive Flow

When the initiative is actually complete and you want to archive it, run:

`python .agents/skills/ub-workflow/scripts/scaffold_initiative.py archive <initiative-root>`

The helper validates completion state first, then moves the initiative under
`../archive/` and synchronizes the initiative index `README.md`.

## Resume Rule

When resuming, read in this order:

1. `./roadmap.md`
2. the latest sprint `closeout.md`
3. the active or next sprint `sprint.md`
4. `./README.md`

Only reopen `./prd.md` if the roadmap or sprint documents are missing needed
initiative context.

## Final Audit

Before treating an initiative as complete:

1. confirm nothing material was missed
2. confirm docs and synchronized artifacts are current where applicable
3. ask whether any follow-up audits or refactors are wanted
4. record that answer
5. write `./retained-note.md`
