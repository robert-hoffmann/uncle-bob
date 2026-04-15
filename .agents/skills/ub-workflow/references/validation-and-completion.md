# Validation and Completion

Use this reference to decide when each initiative phase is complete enough to
move forward.

## PRD Readiness

`prd_ready` is `pass` only when:

1. the problem is clearly defined
2. goals and non-goals are explicit
3. the chosen path is justified
4. at least one alternative was evaluated and rejected
5. success criteria are verifiable
6. dependencies and risks are explicit
7. validation expectations name concrete commands or checks where known
8. documentation touch points are explicit
9. governance bridge level is explicit when governance coordination is needed
10. another operator could continue without chat history

## Roadmap Readiness

`roadmap_ready` is `pass` only when:

1. the roadmap exists and is derived from the current `prd.md`
2. sprint ordering and dependencies are explicit
3. every planned sprint declares path, goal, validation focus, subtasks, and evidence folder
4. the final roadmap item is a final audit
5. the roadmap is rich enough to initialize sprint folders without relying on chat history
6. the agent has surfaced a review checklist covering sprint breakdown completeness, ordering and dependencies, scope boundaries and non-goals, and validation/docs expectations
7. the human explicitly approved the roadmap
8. `README.md` points to sprint initialization as the correct next step
9. repository-specific validation and documentation expectations are explicit where known

## Sprint Initialization

Do not start sprint execution until:

1. the roadmap exists
2. `roadmap_ready` is `pass`
3. all planned sprint folders are initialized
4. each planned sprint has a standalone `sprint.md`
5. each planned sprint includes a concrete validation plan
6. the final roadmap item is a final audit
7. the workflow stops after initialization and waits for an explicit user request before the active sprint begins

## Sprint Closeout

`sprint_closeout` is `pass` only when:

1. planned in-scope work is complete or explicitly blocked
2. known in-scope defects are documented
3. validation results are recorded
4. relevant documentation and synchronized artifacts are updated or explicitly marked unchanged
5. evidence pointers exist when evidence was generated
6. touched workflow documents satisfy ub-quality formatting and structure rules
7. the next sprint can resume from `closeout.md` and `roadmap.md`
8. the workflow is ready to pause for human review before any next sprint work begins

## Initiative Completion

`initiative_complete` is `pass` only when:

1. all implementation sprints have closeout records
2. the final audit ran as the last roadmap item
3. initiative-level validation is recorded and traceable
4. relevant documentation and synchronized artifacts reflect the shipped behavior
5. follow-up audit or refactor decisions were captured
6. `retained-note.md` was written
7. `README.md` and `roadmap.md` reflect the final state
8. touched workflow documents satisfy ub-quality formatting and structure rules
9. the final audit output is ready for human review before any archive action

## Review Questions

When validating an initiative or sprint, ask:

1. could another developer, PM, or agent resume this without prior chat
   history?
2. is the next action explicit?
3. is the current blocker or gate state explicit?
4. are validation expectations concrete instead of implied?
5. are documentation and synchronized artifacts accounted for instead of assumed?
6. do the touched workflow documents satisfy ub-quality formatting and structure rules?
7. is the final audit still present as the terminal roadmap step?
