# Workflow Contract

Use this contract for initiatives that need planning, decomposition, stop-resume
safety, and a durable completion record.

## Lifecycle

Execute work through these phases:

1. discovery and research
2. PRD authoring and refinement
3. roadmap generation
4. sprint initialization
5. ordered sprint execution
6. final audit
7. retained note and closeout

## Initiative-Level Gates

Use these workflow gates:

| Gate                  | Meaning                                               | Allowed States              |
| --------------------- | ----------------------------------------------------- | --------------------------- |
| `prd_ready`           | The PRD is execution-ready and roadmap work can start | `pass`, `fail`, `blocked` |
| `sprint_closeout`     | The active sprint is safe to pause, hand off, or close | `pass`, `fail`, `blocked` |
| `initiative_complete` | The initiative has completed final audit and retained note | `pass`, `fail`, `blocked` |

State intent:

- `pass`: required workflow controls are satisfied
- `fail`: the work was evaluated and one or more controls failed
- `blocked`: the workflow cannot progress yet because prerequisites are missing

## Execution Rules

1. Finish the PRD before generating the roadmap.
2. Generate the full roadmap in one pass.
3. Initialize all sprint folders before sprint execution begins.
4. Keep sprint execution ordered unless the roadmap explicitly allows parallel
   work.
5. Update `roadmap.md` and the initiative `README.md` whenever state changes.
6. Keep the active sprint's `closeout.md` current before pausing.
7. End the roadmap with a final audit step.

## Resume Order

When resuming inside one initiative root, read in this order:

1. `./roadmap.md`
2. the latest sprint `closeout.md`
3. the active or next sprint `sprint.md`
4. `./README.md`
5. `./prd.md` only if initiative-level context is still missing

## Stop-Resume Discipline

Before stopping work, ensure:

1. `README.md` reflects the current phase and next action
2. `roadmap.md` reflects current status and the next action
3. the active sprint has an up-to-date `closeout.md` or is explicitly blocked
4. any generated evidence is stored with the active sprint
5. blockers are written down explicitly

## Final Audit Minimum

The final audit must confirm at minimum:

1. roadmap scope was actually executed
2. no material work was silently skipped
3. synchronized docs, tests, and related artifacts are current where applicable
4. required validation has been run or explicitly deferred
5. the user was asked about follow-up audits or refactors
6. the retained note reflects the final state