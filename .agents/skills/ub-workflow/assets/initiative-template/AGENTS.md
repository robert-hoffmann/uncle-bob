# Initiative Root — AGENTS.md

## Scope

Applies to this initiative root and its descendants.

## Local Rules

- `roadmap.md` is the smallest live progress document for the initiative.
- Read `roadmap.md` first when resuming work.
- Treat each sprint's `sprint.md` as a standalone sprint PRD.
- Do not assume the master `prd.md` must be open to execute a sprint.
- Treat `roadmap.md` as the durable planning artifact after PRD work is done.
- Keep sprint execution sequential unless the roadmap explicitly says otherwise.
- End the roadmap with a mandatory final audit step.

## Resume Order

1. `./roadmap.md`
2. the latest sprint `closeout.md`
3. the active or next sprint `sprint.md`
4. `./README.md`
5. `./prd.md` only if needed for additional initiative-level context

## Update Discipline

- Update `roadmap.md` after every meaningful sprint state change.
- Update `README.md` when blockers, phase, or next step changes.
- Keep the active sprint's `closeout.md` current before stopping work.
- Do not create sprint folders until `roadmap_ready: pass`.
- Create sprint folders from `./sprint-template/` only when initializing the approved roadmap.
- Record the user's follow-up audit or refactor decision before closing the initiative.
