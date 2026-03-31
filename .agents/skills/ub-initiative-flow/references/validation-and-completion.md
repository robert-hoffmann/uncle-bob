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
7. another operator could continue without chat history

## Sprint Initialization

Do not start sprint execution until:

1. the roadmap exists
2. all planned sprint folders are initialized
3. each planned sprint has a standalone `sprint.md`
4. the final roadmap item is a final audit

## Sprint Closeout

`sprint_closeout` is `pass` only when:

1. planned in-scope work is complete or explicitly blocked
2. known in-scope defects are documented
3. validation results are recorded
4. evidence pointers exist when evidence was generated
5. the next sprint can resume from `closeout.md` and `roadmap.md`

## Initiative Completion

`initiative_complete` is `pass` only when:

1. all implementation sprints have closeout records
2. the final audit ran as the last roadmap item
3. follow-up audit or refactor decisions were captured
4. `retained-note.md` was written
5. `README.md` reflects the final state

## Review Questions

When validating an initiative or sprint, ask:

1. could another developer, PM, or agent resume this without prior chat
   history?
2. is the next action explicit?
3. is the current blocker or gate state explicit?
4. are validation expectations concrete instead of implied?
5. is the final audit still present as the terminal roadmap step?