# Sprint Operations — AGENTS.md

## Scope

Applies to this operations root and its descendants.

## Local Rules

- `operation-guide.md` is the formal workflow contract for this operations root.
- `user-guide.md` is the human-facing explanation of the same workflow.
- `roadmap.md` is the small live progress document for an initiative and should
  be the first file read when resuming work.
- `spec.md` is the first file to read when resuming a lightweight spec root.
- Each sprint `sprint.md` must be a standalone sprint PRD that can be executed
  without reopening the master `prd.md`.
- After importing a master PRD, stop and produce a durable `roadmap.md` before
  initializing sprint folders.
- Initialize sprint folders only after `roadmap_ready: pass`.
- After sprint initialization, stop and wait for an explicit user request
  before executing the active sprint.
- The roadmap must end with a final audit step before the initiative can close.
- Validation and documentation are completion gates, not optional follow-up work.
- Keep paths relative to the current operations root or initiative root when
  practical.

## Resume Order For Agents

When resuming work inside one initiative root, read in this order:

1. `./roadmap.md`
2. the most recent sprint `closeout.md`
3. the active or next sprint `sprint.md`
4. `./README.md`
5. `./prd.md` only if additional initiative-level context is still needed

When resuming a lightweight spec root, read `./spec.md` first.

## Update Discipline

- Update `roadmap.md` whenever sprint status changes.
- Update the initiative `README.md` whenever phase, blockers, or next action changes.
- Keep `closeout.md` current before pausing or handing off.
- Do not initialize sprint folders until `roadmap.md` is complete enough to
  stand in for plan output without chat history.
- Initialize sprint folders from the canonical `ub-workflow` sprint template
  when building the roadmap-derived sprint set.
- Execute only the user-requested active sprint in one invocation, then stop
  after closeout and roadmap updates.
- Do not treat a sprint as complete until its validation results, evidence, and
  relevant documentation updates are recorded or explicitly marked unchanged.
- Do not treat an initiative as complete until final validation, retained-note,
  and documentation synchronization checks are recorded.
- Before treating an initiative as complete, record whether the user wants any
  follow-up audits or refactors.
