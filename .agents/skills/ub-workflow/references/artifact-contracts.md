# Artifact Contracts

Use these files as the minimum contract for reusable initiative and
lightweight-spec workflow surfaces.

## Required Initiative Files

- `README.md`: root resume surface and current status
- `AGENTS.md`: local resume order and update discipline
- `prd.md`: self-contained initiative definition
- `roadmap.md`: small live tracker with full sprint order
- `rollup.md`: readable cross-sprint summary and carry-forward surface
- `retained-note.md`: durable completion summary
- `research/`: optional supportive discovery notes, kept secondary to the main
  workflow artifacts
- `exceptions/`: optional bounded exception records, not a catch-all note
  store
- `sprints/`: execution directories and the default home for sprint-local
  evidence and sprint-local decision memory

## `README.md`

Minimum sections:

1. initiative name and owner
2. active interaction mode
3. current phase
4. current gate state
5. roadmap status
6. active sprint or `none`
7. last completed sprint
8. next step
9. blockers
10. governance bridge level and profile when applicable
11. validation pointers
12. smallest file set needed to resume

## `prd.md`

Minimum sections:

1. summary
2. background or problem statement
3. goals
4. non-goals
5. scope
6. principles
7. current-state diagnosis
8. option analysis with chosen path and one rejected alternative
9. success criteria
10. validation expectations
11. documentation touch points
12. governance bridge selection when applicable
13. dependencies and constraints
14. execution risks
15. readiness checklist

## `roadmap.md`

Minimum sections:

1. roadmap objective
2. PRD scope summary
3. overall initiative checklist
4. sprint sequence with one entry per sprint, where every sprint entry declares path, goal, dependencies, validation focus, subtasks, and evidence folder
5. dependency chain across sprints
6. validation focus per sprint
7. current position and next action
8. stop-resume handoff expectation
9. completion condition
10. final audit as the last item

Current-position rule:

1. record the persisted interaction mode alongside current sprint state

Roadmap shape rules:

1. Use as many implementation sprints as the PRD actually requires; do not imply a two-sprint cap.
2. Number implementation sprints sequentially as `Sprint 01` through `Sprint NN`.
3. Keep the final audit as the terminal roadmap item after all implementation sprints.
4. Use `roadmap.md` as the durable post-plan artifact that unlocks sprint initialization.
5. Keep roadmap status explicit enough to distinguish `not started`, `planned`, `generated`, and `complete` when those states matter.

## `sprint.md`

Each sprint document must stand alone.

Treat each `sprint.md` as an execution-ready sprint PRD, not as a starter
shell.

Minimum sections:

1. sprint objective
2. exact scope
3. execution slices
4. dependencies
5. verified repository truth at sprint start
6. chosen implementation path
7. one rejected alternative with concise pros and cons
8. affected files, modules, systems, or docs
9. validation plan
10. mode-specific start checkpoint
11. reviewability check
12. exit criteria
13. final-audit checklist for the final audit sprint
14. handoff expectation
15. definition of done

Sprint document rules:

1. The active or next sprint must be readable and actionable without reopening
 the full initiative chat history.
2. Placeholder-only sprint shells are incomplete planning state, not
 execution-ready artifacts.
3. Execution slices should be the main place where planned work is broken into
 independently reviewable chunks.
4. Each execution slice should name acceptance, verification, dependencies,
   and likely touched areas when those details materially affect execution or
   review.
5. Later sprints may contain named pending handoff markers only in fields that
 legitimately depend on prior closeout truth.
6. The validation plan must be concrete enough for another operator to execute
 it without improvising missing checks.
7. The handoff expectation must name what the next sprint should read first.
8. Use `decision-log.md` for evolving sprint-time decisions, reversals, and
   deferrals instead of forcing all running memory into `closeout.md`.
9. When the active interaction mode is `reviewed`, the sprint document must
   make the pre-sprint preview, option questions when needed, approval
   boundary, and expected post-execution reporting shape easy to recover.
10. For non-trivial reviewed-mode sprints, the mode-specific start checkpoint
   should preserve the richer counterfactual analysis in recoverable order:
   `What Repo Truth Says`, `Inference`, `Implementation Paths`,
   `Recommendation`, then any structured fallback questions needed before
   sprint start approval.
11. For non-trivial reviewed-mode sprints, artifact-update or validation
   bookkeeping may appear in the checkpoint, but it should not be the lead
   user-facing content unless it is itself the repo truth that materially
   shapes the sprint.

## `decision-log.md`

Use this file as the running sprint-level decision-memory surface.

Minimum sections:

1. purpose
2. decisions
3. reversals and deferrals
4. evidence pointers
5. carry forward

Decision-log rules:

1. Keep the log sprint-scoped; repository-level durable decisions still belong
   in `docs/adr/` only when ADR escalation is actually warranted.
2. Record rationale, changed direction, or non-obvious constraints here while
   the sprint is active instead of relying on post-hoc reconstruction in
   `closeout.md`.
3. Link to sprint `evidence/`, touched files, or synchronized artifacts when
   those links materially improve resumability.
4. Keep the file readable; it is a high-signal running log, not a raw command
   dump.

## `closeout.md`

Minimum sections:

1. `environment_note`
2. `scope_note`
3. `decision_note`
4. `gate_note`
5. `exception_note`
6. `validation_note`
7. `done_verification_note`
8. `handoff_note`
9. `follow_up_note`
10. `post_execution_summary_note`

Closeout structure rules:

1. `gate_note` must record the initiative workflow gate state.
2. When governance is active, `gate_note` must also record the governance gate type and result.
3. `validation_note` must capture commands, outcomes, evidence pointers, and documentation-sync status.
4. When governance is active, `exception_note` must reference canonical governance exception metadata.
5. When a sprint used `decision-log.md`, the closeout should leave it current
   enough for the next sprint or final audit to trust it.
6. When the active interaction mode exposes user-facing post-execution
   reporting, the closeout should make considerations moving forward,
   assumptions made, and things to watch easy to recover for later reporting.
7. When the active interaction mode exposes user-facing post-execution
   reporting, `post_execution_summary_note` should be readable enough to reuse
   directly as the user-facing post-sprint summary.

## `rollup.md`

Use this file as the readable initiative-level summary across sprints.

Minimum sections:

1. purpose
2. current snapshot
3. major decisions
4. sprint highlights
5. cross-sprint risks and deferrals
6. validation and evidence rollup
7. research and exceptions pointers

Rollup rules:

1. Keep `rollup.md` shorter and easier to scan than walking every sprint
   directory one by one.
2. Summarize cross-sprint decisions, reversals, and major validation signals
   here, then point to the owning sprint `decision-log.md`, `closeout.md`, or
   `evidence/` when more detail is needed.
3. Do not duplicate every sprint detail verbatim; the rollup is a readable
   index, not a second full archive.
4. Keep `research/` and `exceptions/` visibly secondary by pointing to them
   only when they truly contain cross-sprint discovery or bounded exception
   records.

## `retained-note.md`

Minimum sections:

1. outcome
2. what shipped
3. preserve these decisions
4. useful future notes
5. deferred items
6. follow-up decisions
7. validation baseline

Retained-note rules:

1. When governance is active, record governance bridge level, profile, exception refs, and ADR refs.
2. Validation baseline must be traceable enough for a later operator to reconstruct the final audit posture.
3. Do not pre-fill initiative-specific decisions during scaffold creation; keep the retained note minimal until final audit work begins.

## Lightweight Spec Root

Use lightweight specs for work that sits between direct bounded execution and a
full initiative.

Path contract:

- `./specs/YYYY-MM-DD-slug/spec.md`

Minimum `spec.md` sections:

1. snapshot
2. summary
3. problem or opportunity
4. goals
5. non-goals
6. assumptions and unknowns
7. scale decision
8. chosen path
9. one rejected alternative with concise pros and cons
10. validation plan
11. documentation touch points
12. next action

Lightweight spec rules:

1. The spec must be self-contained enough for another operator to continue
   without chat history.
2. The spec must explain why the work is not merely a direct bounded task and
   why it does not yet require a full initiative.
3. The spec must record what would trigger promotion into a full initiative.
4. The active interaction mode must be explicit in the lightweight spec
   snapshot.
5. Lightweight specs do not require `roadmap.md`, sprint scaffolding, or
   retained-note flow by default.
