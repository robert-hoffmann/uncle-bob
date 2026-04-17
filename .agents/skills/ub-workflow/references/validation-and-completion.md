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

## Research Readiness

`research_ready` is `pass` only when:

1. the current problem or initiative context is grounded enough to support a
   durable PRD
2. open questions that would block PRD authorship are either answered or
   explicitly recorded
3. repository truth checks needed for PRD scope have been completed where known
4. another operator could understand why the initiative exists without relying
   on chat history

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

## Sprint Content Readiness

`sprint_content_ready` is `pass` only when:

1. every planned sprint has a standalone `sprint.md`
2. the active or next sprint is execution-ready rather than a placeholder shell
3. later sprints contain only named pending handoff markers that legitimately
   depend on prior closeout truth
4. each sprint names concrete validation expectations and handoff guidance
5. the sprint pack is rich enough to survive a session reset without relying on
   chat history

## Sprint Initialization

Do not start sprint execution until:

1. the roadmap exists
2. `roadmap_ready` is `pass`
3. all planned sprint folders are initialized
4. `sprint_content_ready` is `pass`
5. each planned sprint has a standalone `sprint.md`
6. each planned sprint includes a concrete validation plan
7. when needed, `sprint_start_ready` is explicit after context refresh
8. the final roadmap item is a final audit
9. the workflow stops after initialization and waits for an explicit user
   request before the active sprint begins

## Sprint Start Readiness

`sprint_start_ready` is `pass` only when:

1. the active or next sprint is execution-ready
2. the smallest required resume file set has been read after any session reset
3. blockers or pending handoff markers have been resolved or explicitly carried
   forward
4. the next action is explicit before implementation begins

## Archive Readiness

`archive_ready` is `pass` only when:

1. `initiative_complete` is effectively satisfied pending explicit human review
2. the final audit output is ready for review
3. `retained-note.md`, `README.md`, and `roadmap.md` reflect the final state
4. archive is being considered explicitly rather than as an automatic side
   effect

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
