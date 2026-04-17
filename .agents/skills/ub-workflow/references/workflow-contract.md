# Workflow Contract

Use this contract for initiatives that need planning, decomposition, stop-resume
safety, and a durable completion record.

## Lifecycle

Execute work through these phases:

1. research and discovery
2. PRD authoring and readiness
3. initiative scaffold and baseline setup
4. roadmap generation and approval
5. sprint-content preparation
6. sprint materialization and start readiness
7. ordered sprint execution
8. sprint closeout and review pause
9. final audit and review pause
10. retained note and archive decision

## Initiative-Level Gates

Use these workflow gates:

| Gate                   | Meaning                                                         | Allowed States            | Ownership                     |
| ---------------------- | --------------------------------------------------------------- | ------------------------- | ----------------------------- |
| `research_ready`       | Discovery is grounded enough to support a durable PRD           | `pass`, `fail`, `blocked` | shared workflow gate          |
| `prd_ready`            | The PRD is execution-ready and roadmap work can start           | `pass`, `fail`, `blocked` | shared workflow gate          |
| `roadmap_ready`        | The roadmap is execution-ready and approved for downstream work | `pass`, `fail`, `blocked` | human-owned review checkpoint |
| `sprint_content_ready` | The sprint pack has execution-ready sprint PRDs                 | `pass`, `fail`, `blocked` | shared workflow gate          |
| `sprint_start_ready`   | The next sprint can begin after context refresh when needed     | `pass`, `fail`, `blocked` | optional shared start gate    |
| `sprint_closeout`      | The active sprint is safe to pause, hand off, or close          | `pass`, `fail`, `blocked` | shared workflow gate          |
| `archive_ready`        | Final audit output is ready for explicit archive review         | `pass`, `fail`, `blocked` | human-owned review checkpoint |
| `initiative_complete`  | The initiative has completed final audit and retained note      | `pass`, `fail`, `blocked` | shared terminal workflow gate |

State intent:

- `pass`: required workflow controls are satisfied
- `fail`: the work was evaluated and one or more controls failed
- `blocked`: the workflow cannot progress yet because prerequisites are missing

Ownership intent:

- `human-owned review checkpoint`: requires explicit user approval or review
   before the workflow advances
- `shared workflow gate`: can be evaluated by the operator or agent, but the
   rationale must be written down in initiative artifacts
- `optional shared start gate`: use when a fresh or resumed sprint needs an
   explicit start-readiness confirmation before execution begins

## Execution Rules

1. Finish or explicitly defer the discovery needed to make the PRD
   self-contained before advancing `prd_ready: pass`.
2. Treat `roadmap.md` as the durable post-plan artifact.
3. Generate the full roadmap in one pass.
4. Surface the roadmap review checklist and wait for explicit human approval
   before setting `roadmap_ready: pass`.
5. Do not prepare sprint content, initialize sprint folders, or begin sprint
   execution until `roadmap_ready: pass`.
6. Prepare each planned sprint as a standalone execution-ready `sprint.md`
   before Sprint 01 or any later sprint begins.
7. Use named pending handoff markers only in sprint fields that legitimately
   depend on prior closeout truth.
8. Materialize or repair sprint folders only after roadmap approval and in a
   way that preserves the prepared sprint content.
9. When a fresh or resumed sprint needs additional context refresh, record that
   checkpoint explicitly before advancing `sprint_start_ready: pass`.
10. Stop after sprint-pack preparation and wait for an explicit user request
    before Sprint 01 or any later sprint begins.
11. Keep sprint execution ordered unless the roadmap explicitly allows parallel
    work.
12. Execute only one user-requested active sprint per invocation.
13. Update `roadmap.md` and the initiative `README.md` whenever state changes.
14. Keep the active sprint's `closeout.md` current before pausing.
15. Stop after every sprint closeout so the human can review before the next
    sprint begins.
16. End the roadmap with a final audit step, then stop for explicit review
    before `archive_ready: pass` or any archive action.
17. Treat the number of implementation sprints as PRD-driven; the roadmap can
    contain `Sprint 01` through `Sprint NN` before the final audit.

## Operations Root Bootstrap

For this repository, the deterministic helper owns operations-root bootstrap.

Rules:

1. If `./.ub-workflows/` is missing, `create` bootstraps it before creating the initiative.
2. The generated operations root does not require a copied local `initiative-template/` directory.
3. The helper must keep the operations-root `README.md` synchronized after create and archive actions.

## Recovery Rules

When the initiative state is partial or inconsistent, prefer the smallest corrective step:

1. missing `./.ub-workflows/`: run the deterministic create flow and bootstrap
   it
2. initiative exists without a copied or refined `./prd.md`: import or
   complete the PRD before planning continues
3. initiative exists without a finished roadmap: complete `roadmap.md` before
   preparing sprint content or initializing sprints
4. roadmap exists but is not yet approved: keep sprint preparation and sprint
   initialization blocked and finish roadmap review first
5. roadmap exists without prepared sprint content: prepare the sprint pack
   before execution continues
6. sprint folders exist but the active or next `sprint.md` is still a
   placeholder shell: block execution and complete sprint preparation first
7. later sprint start depends on prior closeout truth: read the prior
   `closeout.md` and replace any named pending handoff markers that are now
   resolvable
8. archive requested before completion: block the archive and explain the
   missing controls

## Resume Order

When resuming inside one initiative root, read in this order:

1. `./roadmap.md`
2. the most relevant prior sprint `closeout.md` when one exists
3. the active or next sprint `sprint.md`
4. `./README.md`
5. `./prd.md` only if initiative-level context is still missing

## Stop-Resume Discipline

Before stopping work, ensure:

1. `README.md` reflects the current phase and next action
2. `roadmap.md` reflects current status and the next action
3. the active or next sprint has an execution-ready `sprint.md` before any
   sprint start, or the active sprint has an up-to-date `closeout.md` when
   execution has already begun
4. any generated evidence is stored with the active sprint
5. blockers are written down explicitly
6. the human review checkpoint is explicit whenever sprint-pack preparation,
   sprint closeout, or final audit just completed

## Final Audit Minimum

The final audit must confirm at minimum:

1. roadmap scope was actually executed
2. no material work was silently skipped
3. synchronized docs, tests, and related artifacts are current where applicable
4. required validation has been run or explicitly deferred
5. the user was asked about follow-up audits or refactors
6. the retained note reflects the final state
7. archive readiness was surfaced explicitly for human review before any
   archive action
