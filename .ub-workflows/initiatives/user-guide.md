# Human User Guide

## Purpose

This is the quick-start version of the workflow.

Use `operation-guide.md` for the formal rules. Use this file when you want the
short human process.

## The Workflow

1. Start with a scale decision: direct bounded task, lightweight spec, or full initiative.
2. Run `uv run python .agents/skills/ub-workflow/scripts/scaffold_initiative.py create-spec <slug>` for bounded planning work.
3. Run `uv run python .agents/skills/ub-workflow/scripts/scaffold_initiative.py create --prd-source <path-to-prd>` for full initiatives.
4. Confirm `./prd.md` is complete and self-contained.
5. Generate the full `roadmap.md` from that PRD in one pass.
6. If the roadmap is correct, explicitly approve it and mark `roadmap_ready: pass`.
7. Run `uv run python .agents/skills/ub-workflow/scripts/scaffold_initiative.py prepare-sprints <initiative-root>`.
8. Run `uv run python .agents/skills/ub-workflow/scripts/scaffold_initiative.py init-sprints <initiative-root>` when directory materialization is still needed.
9. Stop and wait until the user explicitly asks to execute the active sprint.
10. Execute one sprint at a time.
11. After each sprint, stop for human review before moving to the next sprint.
12. End the roadmap with a final audit.
13. Stop for final human review before archive or other closure actions.
14. Ask whether any follow-up audits or refactors are wanted.
15. Write the retained note.

Fresh scaffold note:

1. a newly scaffolded initiative or lightweight spec can be valid for the
   current phase even when placeholder findings are reported
2. those findings signal later-phase incompleteness unless strict readiness is
   being checked
3. `prepare-sprints` and `init-sprints` still leave the initiative in
   pre-execution state; open the active sprint and review it before starting
   implementation
4. in `reviewed` mode, opening the sprint for review is still not permission
   to execute it; the sprint should stop for a pre-sprint preview of what it
   would do if started now, then resolve any questions that change the sprint
   path, and only
   then ask for explicit approval before execution begins
5. in `reviewed` mode, a request like `Start the next sprint.` opens that
   preview only; execution begins only after a later approval message
6. for non-trivial reviewed-mode sprints, that preview should lead with the
   sprint analysis itself:
   `What Repo Truth Says`, `Inference`, `Implementation Paths`,
   `Recommendation`, then the questions that change the sprint path

## Mental Model

1. `prd.md` explains the whole initiative.
2. `spec.md` is the bounded planning surface between direct execution and a full initiative.
3. `roadmap.md` is the durable post-plan artifact and the small live tracker.
4. Each sprint `sprint.md` is a standalone mini-PRD.
5. The helper bootstraps the operations root if `./.ub-workflows/` does not exist.
6. The helper uses the skill's internal templates, so you do not need to copy a local `initiative-template/` folder into the operations root.
7. Sprint folders are never created during the initial scaffold step.
8. Sprint-pack preparation renders execution-ready sprint PRDs before Sprint 01 begins.
9. Sprint initialization is scaffolding only; it does not start Sprint 01 automatically.
10. `sprint_content_ready: pass` means “ready for execution review,” not “execution already started.”
11. `reviewed` mode adds a distinct pre-sprint preview checkpoint before
    `sprint_start_ready: pass`.
12. for non-trivial reviewed-mode sprints, artifact or validation
    bookkeeping is secondary; the preview should open with repo truth and the
    resulting path decision.
13. The workflow pauses after every sprint and after final audit so the human can review.

## Archive Flow

When the initiative is actually complete and you want to archive it, run:

`uv run python .agents/skills/ub-workflow/scripts/scaffold_initiative.py archive <initiative-root>`

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

When resuming a lightweight spec root, read `./spec.md` first.

## Final Audit

Before treating an initiative as complete:

1. confirm nothing material was missed
2. confirm docs and synchronized artifacts are current where applicable
3. ask whether any follow-up audits or refactors are wanted
4. record that answer
5. write `./retained-note.md`
