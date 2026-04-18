# Workflow Contract

Use this contract for initiatives that need planning, decomposition, stop-resume
safety, and a durable completion record.

## Intake Classification

Start rough work by choosing the smallest lane that can still hold the needed
decisions and validation.

1. direct bounded task: use when the work can be executed safely without a
   durable planning artifact
2. lightweight spec: use when the work needs assumptions, scope, options, and
   validation written down, but does not justify a roadmap and sprint pack
3. initiative: use when the work is multi-session, risky, cross-cutting, or
   needs a PRD, roadmap, and resumable sprint execution model

The lifecycle below applies to initiative work. Lightweight specs are a
bounded alternative path, not a weakened initiative lane.

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

## Interaction Modes

Interaction mode is a workflow-behavior layer, not a readiness layer.

Lane decides which artifacts and readiness checks are required.
Mode decides how execution is surfaced to the user once that lane is actually
ready.

Mode precedence:

1. explicit user turn override
2. persisted artifact mode
3. default fallback = `reviewed`

Persistence:

1. initiative lane: persist mode in initiative artifacts
2. lightweight-spec lane: persist mode in `spec.md`
3. direct bounded lane: runtime only unless the work is promoted into a
   durable artifact

Canonical modes:

1. `reviewed`
   - user-facing pre-execution analysis
   - user-facing post-execution reporting
   - mandatory pause between sprints or bounded execution chunks
2. `flow`
   - short user-facing pre-execution note
   - richer user-facing post-execution reporting
   - no pre-execution pause, but manual advancement after each sprint or
     bounded execution chunk
3. `auto`
   - internal pre-execution analysis by default
   - concise user-facing post-execution reporting
   - automatic advancement unless interruption conditions are met
4. `continuous`
   - user-facing alias: `yolo`
   - internal analysis and artifact updates still required
   - no routine user-facing pre/post-execution reporting
   - no routine pause between sprints or bounded execution chunks
   - interrupt only when a major blocker or conflict requires aborting or
     pausing the work

Question handling:

1. prefer `AskUserQuestion` / `vscode/askQuestions` when the host exposes it
2. always allow a custom reply path
3. when the question tool is unavailable, use the same text structure:
   `(*)` on the best qualitative fit, a short explanation under every option
   in `(...)`, and a final `Custom` option

Mode reporting:

1. user-facing execution contexts should include a concise mode reference so
   the user does not need to search the docs for the mode names
2. user-facing post-execution reporting should cover what changed, why it
   mattered, considerations moving forward, assumptions made, and things to
   watch whenever the active mode surfaces post-execution reporting

## Execution Rules

1. Finish or explicitly defer the discovery needed to make the PRD
   self-contained before advancing `prd_ready: pass`.
2. Make the scale decision explicit before opening initiative artifacts:
   direct bounded task, lightweight spec, or initiative.
3. Do not route rough ideas into a full initiative when a direct bounded task
   or lightweight spec is sufficient.
4. Use a lightweight spec under `./.ub-workflows/specs/YYYY-MM-DD-slug/spec.md`
   when the work needs a durable contract without roadmap and sprint overhead.
5. Treat `roadmap.md` as the durable post-plan artifact.
6. Generate the full roadmap in one pass.
7. Surface the roadmap review checklist and wait for explicit human approval
   before setting `roadmap_ready: pass`.
8. Do not prepare sprint content, initialize sprint folders, or begin sprint
   execution until `roadmap_ready: pass`.
9. Prepare each planned sprint as a standalone execution-ready `sprint.md`
   before Sprint 01 or any later sprint begins.
10. During sprint preparation, expand roadmap subtasks into richer execution
    slices in the sprint plan rather than leaving the sprint as a flat checklist.
11. Use named pending handoff markers only in sprint fields that legitimately
   depend on prior closeout truth.
12. Materialize or repair sprint folders only after roadmap approval and in a
   way that preserves the prepared sprint content.
13. When a fresh or resumed sprint needs additional context refresh, record that
   checkpoint explicitly before advancing `sprint_start_ready: pass`.
14. Stop after sprint-pack preparation and wait for an explicit user request
    before Sprint 01 or any later sprint begins.
15. Keep sprint execution ordered unless the roadmap explicitly allows parallel
    work.
16. Resolve and honor the active interaction mode before execution begins.
17. For initiative sprint execution, every mode requires the same readiness
    prerequisites: approved roadmap, prepared sprint pack, execution-ready
    current sprint, and no unresolved blockers preventing safe execution.
18. Use each sprint's `decision-log.md` as the running sprint-level memory
    surface and use `rollup.md` as the readable initiative-level carry-forward
    summary.
19. Keep `research/` supportive and cross-sprint in character, and keep
    `exceptions/` bounded and explicit instead of treating either folder as a
    generic note dump.
20. Update `roadmap.md`, the initiative `README.md`, and `rollup.md` whenever
    state changes materially affect later resume work.
21. Keep the active sprint's `decision-log.md` and `closeout.md` current before
    pausing.
22. Materialize newly introduced additive workflow files in existing sprint
    folders from the canonical `ub-workflow` sprint template when it evolves,
    without overwriting prepared sprint content.
23. `reviewed` and `flow` stop after every sprint closeout so the human can
    review before the next sprint begins.
24. `auto` may continue after sprint closeout unless a hard blocker, material
    ambiguity, repo-truth conflict, or later-sprint-shaping decision requires
    interruption.
25. `continuous` / `yolo` may continue without routine user-facing reporting,
    but must abort or pause when a major blocker or conflict requires explicit
    user resolution, and that interruption must be documented clearly.
26. End the roadmap with a final audit step, then stop for explicit review
    before `archive_ready: pass` or any archive action.
27. Treat the number of implementation sprints as PRD-driven; the roadmap can
    contain `Sprint 01` through `Sprint NN` before the final audit.

## Operations Root Bootstrap

For this repository, the deterministic helper owns operations-root bootstrap.

Rules:

1. If `./.ub-workflows/` is missing, `create` bootstraps it before creating the initiative.
2. The generated operations root does not require a copied local `initiative-template/` directory.
3. The helper must keep the operations-root `README.md` synchronized after create and archive actions.

## Recovery Rules

When the initiative state is partial or inconsistent, prefer the smallest corrective step:

1. rough idea without a clear lane: make the scale decision before opening PRD
   or roadmap work
2. missing `./.ub-workflows/`: run the deterministic create flow and bootstrap
   it
3. initiative exists without a copied or refined `./prd.md`: import or
   complete the PRD before planning continues
4. initiative exists without a finished roadmap: complete `roadmap.md` before
   preparing sprint content or initializing sprints
5. roadmap exists but is not yet approved: keep sprint preparation and sprint
   initialization blocked and finish roadmap review first
6. roadmap exists without prepared sprint content: prepare the sprint pack
   before execution continues
7. sprint folders exist but the active or next `sprint.md` is still a
   placeholder shell: block execution and complete sprint preparation first
8. later sprint start depends on prior closeout truth: read the prior
   `closeout.md` and replace any named pending handoff markers that are now
   resolvable
9. initiative or sprint memory surfaces are missing after template evolution:
   backfill `rollup.md` or sprint `decision-log.md` from the canonical
   templates before continuing
10. archive requested before completion: block the archive and explain the
   missing controls

## Resume Order

When resuming inside one initiative root, read in this order:

1. `./roadmap.md`
2. `./rollup.md` when it exists
3. the most relevant prior sprint `closeout.md` when one exists
4. the active or next sprint `sprint.md`
5. the active sprint `decision-log.md` when one exists and the sprint is in
   progress
6. `./README.md`
7. `./prd.md` only if initiative-level context is still missing

When resuming a lightweight spec root, read `./spec.md` first.

## Stop-Resume Discipline

Before stopping work, ensure:

1. `README.md` reflects the current phase and next action
2. `roadmap.md` reflects current status and the next action
3. the active or next sprint has an execution-ready `sprint.md` before any
   sprint start, or the active sprint has an up-to-date `closeout.md` when
   execution has already begun
4. `rollup.md` reflects any cross-sprint decision, validation, or deferral
   changes that materially affect later work
5. the active sprint's `decision-log.md` is current enough to explain the
   running state
6. any generated evidence is stored with the active sprint
7. blockers are written down explicitly
8. the human review checkpoint is explicit whenever sprint-pack preparation,
   sprint closeout, or final audit just completed

## Final Audit Minimum

The final audit must confirm at minimum:

1. roadmap scope was actually executed
2. no material work was silently skipped
3. synchronized docs, tests, and related artifacts are current where applicable
4. required validation has been run or explicitly deferred
5. the user was asked about follow-up audits or refactors
6. the retained note reflects the final state
7. `rollup.md` reflects the final cross-sprint summary
8. archive readiness was surfaced explicitly for human review before any
   archive action
