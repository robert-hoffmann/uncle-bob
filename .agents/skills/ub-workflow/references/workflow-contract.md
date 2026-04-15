# Workflow Contract

Use this contract for initiatives that need planning, decomposition, stop-resume
safety, and a durable completion record.

## Lifecycle

Execute work through these phases:

1. discovery and research
2. PRD authoring and refinement
3. roadmap planning and approval
4. sprint initialization
5. ordered sprint execution
6. final audit
7. retained note and closeout

## Initiative-Level Gates

Use these workflow gates:

| Gate                  | Meaning                                               | Allowed States              |
| --------------------- | ----------------------------------------------------- | --------------------------- |
| `prd_ready`           | The PRD is execution-ready and roadmap work can start | `pass`, `fail`, `blocked` |
| `roadmap_ready`       | The roadmap is execution-ready and sprint initialization can start | `pass`, `fail`, `blocked` |
| `sprint_closeout`     | The active sprint is safe to pause, hand off, or close | `pass`, `fail`, `blocked` |
| `initiative_complete` | The initiative has completed final audit and retained note | `pass`, `fail`, `blocked` |

State intent:

- `pass`: required workflow controls are satisfied
- `fail`: the work was evaluated and one or more controls failed
- `blocked`: the workflow cannot progress yet because prerequisites are missing

## Execution Rules

1. Finish the PRD before generating the roadmap.
2. Treat `roadmap.md` as the durable post-plan artifact.
3. Generate the full roadmap in one pass.
4. Surface the roadmap review checklist and wait for explicit human approval before setting `roadmap_ready: pass`.
5. Do not materialize sprint folders until `roadmap_ready: pass`.
6. Materialize all sprint folders from the completed roadmap before sprint execution begins.
7. Stop after sprint initialization and wait for an explicit user request before starting Sprint 01 or any later sprint.
8. Keep sprint execution ordered unless the roadmap explicitly allows parallel
   work.
9. Execute only one user-requested active sprint per invocation.
10. Update `roadmap.md` and the initiative `README.md` whenever state changes.
11. Keep the active sprint's `closeout.md` current before pausing.
12. Stop after every sprint closeout so the human can review before the next sprint begins.
13. End the roadmap with a final audit step.
14. Stop after final audit so the human can review before archive or other closure actions.
15. Treat the number of implementation sprints as PRD-driven; the roadmap can contain `Sprint 01` through `Sprint NN` before the final audit.

## Operations Root Bootstrap

For this repository, the deterministic helper owns operations-root bootstrap.

Rules:

1. If `./.ub-workflows/` is missing, `create` bootstraps it before creating the initiative.
2. The generated operations root does not require a copied local `initiative-template/` directory.
3. The helper must keep the operations-root `README.md` synchronized after create and archive actions.

## Recovery Rules

When the initiative state is partial or inconsistent, prefer the smallest corrective step:

1. missing `./.ub-workflows/`: run the deterministic create flow and bootstrap it
2. initiative exists without a copied or refined `./prd.md`: import or complete the PRD before planning continues
3. initiative exists without a finished roadmap: complete `roadmap.md` before initializing sprints
4. roadmap exists but is not yet approved: keep sprint initialization blocked and finish roadmap review first
5. roadmap exists without sprint folders: run `init-sprints`
6. sprint folders exist but are incomplete: repair the missing template files before execution continues
7. archive requested before completion: block the archive and explain the missing controls

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
6. the human review checkpoint is explicit whenever sprint initialization,
   sprint closeout, or final audit just completed

## Final Audit Minimum

The final audit must confirm at minimum:

1. roadmap scope was actually executed
2. no material work was silently skipped
3. synchronized docs, tests, and related artifacts are current where applicable
4. required validation has been run or explicitly deferred
5. the user was asked about follow-up audits or refactors
6. the retained note reflects the final state
