# Initiative Root — AGENTS.md

## Scope

Applies to this initiative root and its descendants.

## Local Rules

- `roadmap.md` is the smallest live progress document for the initiative.
- `rollup.md` is the readable cross-sprint summary, not a replacement for
  sprint-local truth.
- Read `roadmap.md` first when resuming work.
- Treat each sprint's `sprint.md` as a standalone sprint PRD.
- Treat each sprint's `decision-log.md` as the running sprint-level memory
  surface.
- Do not assume the master `prd.md` must be open to execute a sprint.
- Treat `roadmap.md` as the durable planning artifact after PRD work is done.
- Keep sprint execution sequential unless the roadmap explicitly says otherwise.
- End the roadmap with a mandatory final audit step.
- Keep `research/` supportive and bounded; do not use it as a general sprint
  note store.
- Keep `exceptions/` for explicit exception records only.

## Resume Order

1. `./roadmap.md`
2. `./rollup.md`
3. the latest sprint `closeout.md`
4. the active or next sprint `sprint.md`
5. the active sprint `decision-log.md` when it materially affects execution
6. `./README.md`
7. `./prd.md` only if needed for additional initiative-level context

## Update Discipline

- Update `roadmap.md` after every meaningful sprint state change.
- Update `rollup.md` when a sprint materially changes cross-sprint direction,
  assumptions, or validation posture.
- Update `README.md` when blockers, phase, or next step changes.
- Keep the active sprint's `decision-log.md` current during execution.
- Keep the active sprint's `closeout.md` current before stopping work.
- Do not create sprint folders until `roadmap_ready: pass`.
- Create sprint folders from the canonical `ub-workflow` sprint template only
  when initializing the approved roadmap.
- Record the user's follow-up audit or refactor decision before closing the initiative.
