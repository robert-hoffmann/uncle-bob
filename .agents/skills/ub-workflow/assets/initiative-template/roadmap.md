# Sprint Roadmap

Status: REPLACE_CURRENT_STATUS

This is the small live progress document for the initiative.

Generate the full ordered sprint roadmap from `./prd.md` before starting sprint
execution, review it until `roadmap_ready: pass`, then keep this file current
as the initiative moves forward.

## Overall Checklist

- [ ] Master PRD imported into `./prd.md`
- [ ] Master roadmap generated from `./prd.md`
- [ ] Roadmap reviewed and approved with `roadmap_ready: pass`
- [ ] All sprint folders initialized under `./sprints/` from the canonical `ub-workflow` sprint template
- [ ] Sprint execution started
- [ ] All sprint closeouts completed
- [ ] Final audit completed as the last roadmap item
- [ ] Follow-up audit or refactor decision recorded
- [ ] `./retained-note.md` written

## Current Position

- Interaction mode: `reviewed`
- Current sprint: `none`
- Last completed sprint: `none`
- Next sprint: REPLACE_NEXT_SPRINT
- Resume from: REPLACE_RESUME_FROM
- Active blockers: `none`

## Roadmap Objective

Replace with the initiative objective.

## PRD Scope Summary

In scope:

1. Replace with the first in-scope area.
2. Replace with the second in-scope area.

Out of scope:

1. Replace with the first out-of-scope area.
2. Replace with the second out-of-scope area.

## Sprint Sequence

The number of implementation sprints is PRD-driven.

Repeat the implementation sprint entry shape below for Sprint 01 through Sprint NN-1 as needed, then keep the final audit as the last roadmap item.

Do not run `prepare-sprints` or `init-sprints` until this roadmap is complete,
reviewed, and the initiative `README.md` records `roadmap_ready: pass`.

- [ ] Sprint 01 - Replace with sprint title
  - Path: `./sprints/01-replace-me/sprint.md`
  - Goal: Replace with sprint goal
  - Depends on: `none`
  - Validation focus: Replace with validation focus
  - Subtasks:
    - [ ] Replace with subtask
    - [ ] Replace with subtask
  - Evidence folder: `./sprints/01-replace-me/evidence/`

- [ ] Sprint 02 through Sprint NN-1 - Repeat this entry shape as many times as the PRD requires
  - Path: `./sprints/NN-replace-me/sprint.md`
  - Goal: Replace with sprint goal
  - Depends on: `Sprint NN-1 - Replace with prior sprint title` or `none` when parallel work is explicitly allowed
  - Validation focus: Replace with validation focus
  - Subtasks:
    - [ ] Replace with subtask
    - [ ] Replace with subtask
  - Evidence folder: `./sprints/NN-replace-me/evidence/`

- [ ] Final Audit - Replace with audit title
  - Path: `./sprints/NN-final-audit/sprint.md`
  - Goal: verify full implementation completeness, synchronization, and follow-up needs
  - Depends on: `all prior implementation sprints`
  - Validation focus: completeness review, documentation synchronization, final quality gates, and follow-up audit/refactor review
  - Subtasks:
    - [ ] Confirm no material roadmap scope was missed
    - [ ] Confirm documentation and synchronized artifacts are current where applicable
    - [ ] Ask whether follow-up audits or refactors are wanted and record the answer
  - Evidence folder: `./sprints/NN-final-audit/evidence/`

## Dependency Chain

1. Replace with the dependency chain between Sprint 01 and Sprint NN.

## Validation Focus Per Sprint

1. Sprint 01: Replace with the sprint validation focus.
2. Sprint 02 through Sprint NN-1: Replace with the sprint validation focus for each planned implementation sprint.
3. Final Audit: completeness review, synchronized artifacts, final validation gates, and follow-up review.

## Final Audit Step

The final audit must confirm at minimum:

1. roadmap scope was actually executed
2. no material work was silently skipped
3. synchronized docs, tests, and related artifacts are current where applicable
4. required validation has been run or explicitly deferred
5. the user was asked about follow-up audits or refactors
6. the retained note reflects the final state

## Handoff Expectations

1. Resume from `./roadmap.md` first, then open the active or next sprint's `sprint.md`, then the latest `closeout.md` once execution has begun.
2. Keep each sprint `sprint.md` standalone so execution does not depend on chat history or reopening the master `prd.md`.
3. Save deterministic evidence under the active sprint's `./evidence/` folder before changing sprint state.
4. Update this roadmap and `./README.md` after every meaningful sprint status change.

## Initiative Completion Condition

The initiative is complete only when:

1. all roadmap items have closeout records
2. the final audit sprint ends with a passing completion decision
3. required validation scenarios are covered and traceable
4. the canonical docs and synchronized artifacts are current
5. `./retained-note.md` has been written with the final follow-up decision
