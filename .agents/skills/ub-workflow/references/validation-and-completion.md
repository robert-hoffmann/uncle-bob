# Validation and Completion

Use this reference to decide when each initiative phase is complete enough to
move forward.

## PRD Readiness

`prd_ready` is `pass` only when:

1. the problem is clearly defined
2. goals and non-goals are explicit
3. assumptions, constraints, and unknowns that shape the PRD are explicit
4. the chosen path is justified
5. at least one alternative was evaluated and rejected
6. success criteria are verifiable
7. dependencies and risks are explicit
8. validation expectations name concrete commands or checks where known
9. documentation touch points are explicit
10. governance bridge level is explicit when governance coordination is needed
11. another operator could continue without chat history

## Lightweight Spec Readiness

A lightweight spec is ready only when:

1. the work is explicitly bounded and does not need a full roadmap and sprint
   pack yet
2. the problem, goals, and non-goals are explicit
3. assumptions, constraints, and unknowns are explicit
4. the chosen path is justified
5. at least one alternative was evaluated and rejected
6. validation expectations are concrete instead of implied
7. documentation touch points are explicit when they matter
8. the boundary to direct bounded work and the promotion trigger to a full
   initiative are explicit
9. the next action is explicit
10. another operator could continue without chat history
11. the active interaction mode is explicit when the spec will drive
    user-facing or resumable execution behavior

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
10. the initiative interaction mode is explicit in the initiative status
    surfaces when the initiative will drive sprint execution

## Sprint Content Readiness

`sprint_content_ready` is `pass` only when:

1. every planned sprint has a standalone `sprint.md`
2. every planned sprint has a `decision-log.md` available for running
   sprint-level memory
3. the active or next sprint is execution-ready rather than a placeholder shell
4. the active or next sprint breaks work into reviewable execution slices
5. the active or next sprint makes acceptance and verification explicit for
   those slices instead of leaving success implied
6. later sprints contain only named pending handoff markers that legitimately
   depend on prior closeout truth
7. each sprint names concrete validation expectations and handoff guidance
8. the sprint pack is rich enough to survive a session reset without relying on
   chat history

## Sprint Initialization

Do not start sprint execution until:

1. the roadmap exists
2. `roadmap_ready` is `pass`
3. all planned sprint folders are initialized
4. `sprint_content_ready` is `pass`
5. each planned sprint has a standalone `sprint.md`
6. each planned sprint has a `decision-log.md`
7. each planned sprint includes a concrete validation plan
8. when needed, `sprint_start_ready` is explicit after context refresh
9. the final roadmap item is a final audit
10. the workflow stops after initialization and waits for an explicit user
   request before the active sprint begins

## Sprint Start Readiness

`sprint_start_ready` is `pass` only when:

1. the active or next sprint is execution-ready
2. the smallest required resume file set has been read after any session reset
3. blockers or pending handoff markers have been resolved or explicitly carried
   forward
4. the next action is explicit before implementation begins
5. the execution slices are reviewable enough that another operator could pick
   a slice and start work without re-planning the sprint
6. the sprint `decision-log.md` exists and is ready to absorb running
   decisions as execution proceeds
7. the active interaction mode is explicit and does not conflict with the
   current initiative status artifacts

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
7. the active sprint `decision-log.md` reflects the material sprint decisions,
   reversals, or deferrals
8. `rollup.md` is updated or explicitly left unchanged when the sprint did not
   materially affect cross-sprint understanding
9. the next sprint can resume from `closeout.md`, `decision-log.md`, and
   `roadmap.md`
10. the workflow's next-step behavior matches the active interaction mode
11. when the active interaction mode surfaces user-facing post-execution
    reporting, considerations moving forward and things to watch are explicit

## Initiative Completion

`initiative_complete` is `pass` only when:

1. all implementation sprints have closeout records
2. the final audit ran as the last roadmap item
3. initiative-level validation is recorded and traceable
4. relevant documentation and synchronized artifacts reflect the shipped behavior
5. follow-up audit or refactor decisions were captured
6. `retained-note.md` was written
7. `rollup.md`, `README.md`, and `roadmap.md` reflect the final state
8. touched workflow documents satisfy ub-quality formatting and structure rules
9. the final audit output is ready for human review before any archive action
10. the recorded interaction mode history does not contradict the final
    initiative state

## Review Questions

When validating an initiative or sprint, ask:

1. could another developer, PM, or agent resume this without prior chat
   history?
2. is the next action explicit?
3. is the current blocker or gate state explicit?
4. was the scale decision intentional: direct bounded task, lightweight spec,
   or initiative?
5. are validation expectations concrete instead of implied?
6. are documentation and synchronized artifacts accounted for instead of assumed?
7. do the touched workflow documents satisfy ub-quality formatting and structure rules?
8. is the final audit still present as the terminal roadmap step?
