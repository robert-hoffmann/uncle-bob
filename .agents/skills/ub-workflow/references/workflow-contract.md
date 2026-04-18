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
   - user-facing pre-sprint preview as a distinct sprint-start checkpoint
   - the preview evaluates what the sprint would do if it started now, before
     any implementation begins
   - non-trivial sprints should surface multiple implementation paths with
     concise pros and cons plus a recommended path
   - questions that change the sprint path should be resolved before execution
     using the structured question fallback when needed
   - explicit human approval before execution or `sprint_start_ready: pass`
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
   in `(...)`, and a final `Custom` option.
4. when text questions are used for a reviewed-mode pre-sprint preview, keep
   the same decision structure as the canonical reviewed-mode pre-sprint
   preview pattern below.
5. In `reviewed` mode, resolve the questions that change the sprint path
   before the explicit start-approval question.
   A request like `Start the next sprint.` opens the preview, but it does not
   count as sprint-start approval in the same turn.

Mode reporting:

1. user-facing execution contexts should include a concise mode reference so
   the user does not need to search the docs for the mode names
2. in `reviewed` mode, the pre-sprint preview should explicitly say the sprint
   has not started yet and should explain what the sprint would do if it
   started now
3. for non-trivial reviewed-mode sprints, that preview should surface at least
   two plausible implementation paths with concise pros and cons plus a
   recommended path
4. in `reviewed` mode, the preview should make the active sprint, chosen path,
   approval boundary, and any questions that change the sprint path explicit
   before execution begins
5. for non-trivial reviewed-mode sprints, lead the user-facing preview with
   the actual sprint analysis rather than artifact-update or validation
   bookkeeping; artifact sync notes are secondary and should not be the opener
6. user-facing post-execution reporting should cover what changed, why it
   mattered, considerations moving forward, assumptions made, and things to
   watch whenever the active mode surfaces post-execution reporting

## Reviewed-Mode Pre-Sprint Preview Pattern

This is the canonical reviewed-mode sprint-start pattern.
Other workflow surfaces should summarize it, not redefine it.

Always required:

1. state that the sprint is still in pre-sprint mode
2. state that no implementation has started yet
3. explain what the sprint would do if it started now
4. name the intended or recommended path
5. state the approval boundary explicitly
6. state that execution begins only after a later approval message, not from
   the same start request that opened the preview

Required only for non-trivial reviewed-mode sprints:

1. lead with the actual sprint analysis, not artifact-update or validation
   bookkeeping
2. include a `What Repo Truth Says` section that captures the current repo
   facts that materially shape the sprint
3. include an `Inference` section that explains what those facts mean for the
   sprint now
4. include an `Implementation Paths` section with at least two plausible paths
5. include concise pros and cons for each path
6. mark the recommended path with `(*)`
7. include a `Recommendation` section that explains why the recommended path
   is currently the best fit
8. ask the questions that change the sprint path before asking for explicit
   sprint-start approval
9. close with the explicit approval boundary and a no-edits-yet statement

Treat a sprint as non-trivial when any of these are true:

1. more than one plausible path would materially change scope, ordering,
   touched surfaces, or later sprints
2. the sprint touches shared contracts, governance boundaries, or other
   cross-cutting behavior
3. the user could reasonably want to steer the path before execution starts

Compact example:

```text
Sprint 03 is still in pre-sprint mode only.
No implementation has started.

If we started this sprint now, the job would be to tighten governance-owned
guidance around the minimum durable record without changing the governance
model.

What Repo Truth Says

- The governance model is already coherent enough for normal initiative work.
- The remaining friction is that “minimum durable record” is still slower to
  infer than it should be.
- The repo does not need a new governance system; it needs faster operator
  guidance.

Inference

This sprint should stay narrow and calibrate governance-owned guidance rather
than widen into command-policy cleanup or catalog-wide consistency work.

Implementation Paths

`A` (*) narrow owner-surface calibration
(Best fit because it solves the fast-path problem directly without widening
scope.)
`B` broader governance-surface harmonization
(Pros: more complete in one pass. Cons: blends into later consistency work.)
`Custom`

Recommendation

`A` is the strongest fit because it improves the operator fast path without
quietly redesigning governance.

Questions That Change The Sprint Path

Which path should this sprint use before it starts?

Start approval:
I have not started Sprint 03.
This preview turn does not start execution.
Execution would begin only after a later approval message that approves
path `A`.

No files were edited in this pre-sprint evaluation step.
```

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
14. In `reviewed` mode, surface a distinct pre-sprint preview checkpoint before
    execution begins.
15. That preview must make explicit that no implementation has started yet,
    explain what the sprint would do if started now, surface alternatives when
    the sprint is non-trivial, and ask any questions that change the sprint
    path needed to calibrate the sprint path.
16. For non-trivial reviewed-mode sprints, that preview should lead with the
    sprint analysis itself:
    `What Repo Truth Says`, `Inference`, `Implementation Paths`,
    `Recommendation`, then the questions that change the sprint path.
    Do not lead the user-facing preview with artifact-update or validation
    bookkeeping.
17. Wait for explicit human approval only after the reviewed-mode preview and
    its questions are resolved, then advance `sprint_start_ready: pass` or
    start the sprint.
18. In `reviewed` mode, that approval must come in a later user reply after
    the preview is shown.
    Do not infer sprint-start approval from the same user turn that requested
    the sprint start.
19. Stop after sprint-pack preparation and wait for an explicit user request
    before Sprint 01 or any later sprint begins.
20. Keep sprint execution ordered unless the roadmap explicitly allows parallel
    work.
21. Resolve and honor the active interaction mode before execution begins.
22. For initiative sprint execution, every mode requires the same readiness
    prerequisites: approved roadmap, prepared sprint pack, execution-ready
    current sprint, and no unresolved blockers preventing safe execution.
23. Use each sprint's `decision-log.md` as the running sprint-level memory
    surface and use `rollup.md` as the readable initiative-level carry-forward
    summary.
24. Keep `research/` supportive and cross-sprint in character, and keep
    `exceptions/` bounded and explicit instead of treating either folder as a
    generic note dump.
25. Update `roadmap.md`, the initiative `README.md`, and `rollup.md` whenever
    state changes materially affect later resume work.
26. Keep the active sprint's `decision-log.md` and `closeout.md` current before
    pausing.
27. When the active mode surfaces post-execution reporting, write a recoverable
    post-execution summary into `closeout.md` before the workflow pauses or
    advances.
28. Materialize newly introduced additive workflow files in existing sprint
    folders from the canonical `ub-workflow` sprint template when it evolves,
    without overwriting prepared sprint content.
29. `reviewed` and `flow` stop after every sprint closeout so the human can
    review before the next sprint begins.
30. `auto` may continue after sprint closeout unless a hard blocker, material
    ambiguity, repo-truth conflict, or later-sprint-shaping decision requires
    interruption.
31. `continuous` / `yolo` may continue without routine user-facing reporting,
    but must abort or pause when a major blocker or conflict requires explicit
    user resolution, and that interruption must be documented clearly.
32. End the roadmap with a final audit step, then stop for explicit review
    before `archive_ready: pass` or any archive action.
33. Treat the number of implementation sprints as PRD-driven; the roadmap can
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
