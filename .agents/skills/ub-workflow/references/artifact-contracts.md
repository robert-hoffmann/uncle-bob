# Artifact Contracts

Use these files as the minimum contract for a reusable initiative workflow.

## Required Initiative Files

| Artifact           | Purpose                                      |
| ------------------ | -------------------------------------------- |
| `README.md`        | Root resume surface and current status       |
| `AGENTS.md`        | Local resume order and update discipline     |
| `prd.md`           | Self-contained initiative definition         |
| `roadmap.md`       | Small live tracker with full sprint order    |
| `retained-note.md` | Durable completion summary                   |
| `research/`        | Optional discovery notes and supporting inputs |
| `exceptions/`      | Optional bounded exception records           |
| `sprints/`         | Execution directories                        |
| `sprint-template/` | Canonical template used to seed each sprint  |

## `README.md`

Minimum sections:

1. initiative name and owner
2. current phase
3. current gate state
4. roadmap status
5. active sprint or `none`
6. last completed sprint
7. next step
8. blockers
9. governance bridge level and profile when applicable
10. validation pointers
11. smallest file set needed to resume

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

Roadmap shape rules:

1. Use as many implementation sprints as the PRD actually requires; do not imply a two-sprint cap.
2. Number implementation sprints sequentially as `Sprint 01` through `Sprint NN`.
3. Keep the final audit as the terminal roadmap item after all implementation sprints.
4. Use `roadmap.md` as the durable post-plan artifact that unlocks sprint initialization.
5. Keep roadmap status explicit enough to distinguish `not started`, `planned`, `generated`, and `complete` when those states matter.

## `sprint.md`

Each sprint document must stand alone.

Minimum sections:

1. sprint objective
2. exact scope
3. dependencies
4. verified repository truth at sprint start
5. chosen implementation path
6. one rejected alternative with concise pros and cons
7. affected files, modules, systems, or docs
8. validation plan
9. exit criteria
10. final-audit checklist for the final audit sprint
11. handoff expectation
12. definition of done

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

Closeout structure rules:

1. `gate_note` must record the initiative workflow gate state.
2. When governance is active, `gate_note` must also record the governance gate type and result.
3. `validation_note` must capture commands, outcomes, evidence pointers, and documentation-sync status.
4. When governance is active, `exception_note` must reference canonical governance exception metadata.

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
