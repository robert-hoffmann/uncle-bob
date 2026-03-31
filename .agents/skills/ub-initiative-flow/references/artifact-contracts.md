# Artifact Contracts

Use these files as the minimum contract for a reusable initiative workflow.

## Required Initiative Files

| Artifact           | Purpose |
| ------------------ | ------- |
| `README.md`        | Root resume surface and current status |
| `AGENTS.md`        | Local resume order and update discipline |
| `prd.md`           | Self-contained initiative definition |
| `roadmap.md`       | Small live tracker with full sprint order |
| `retained-note.md` | Durable completion summary |
| `research/`        | Optional discovery notes and supporting inputs |
| `exceptions/`      | Optional bounded exception records |
| `sprints/`         | Execution directories |
| `sprint-template/` | Canonical template used to seed each sprint |

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
9. validation pointers
10. smallest file set needed to resume

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
10. dependencies and constraints
11. execution risks
12. readiness checklist

## `roadmap.md`

Minimum sections:

1. roadmap objective
2. PRD scope summary
3. overall initiative checklist
4. sprint sequence with one entry per sprint
5. dependency chain across sprints
6. validation focus per sprint
7. current position and next action
8. stop-resume handoff expectation
9. completion condition
10. final audit as the last item

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
10. handoff expectation
11. definition of done

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

## `retained-note.md`

Minimum sections:

1. outcome
2. what shipped
3. preserve these decisions
4. useful future notes
5. deferred items
6. follow-up decisions
7. validation baseline