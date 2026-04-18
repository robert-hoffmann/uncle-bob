# Sprint Closeout

## environment_note

Replace with the runtime and environment context for this sprint.

## scope_note

Replace with what this sprint evaluated, what stayed out of scope, and the
governance bridge level or profile when governance coordination was active.

## decision_note

Replace with the chosen path and one rejected alternative with concise pros and cons.

## gate_note

Replace with the initiative workflow gate state as
`sprint_closeout: pass|fail|blocked` and why.

When governance is active, also record the governance gate type and result as
`merge|confidence|release: pass|fail|blocked`.

## exception_note

Replace with active exceptions or `none`.

When governance is active, reference exception records that use the canonical
governance exception metadata.

## validation_note

Replace with the validation commands or checks and their outcomes.

Also record any documentation or synchronized-artifact validation that was required for this sprint.

When tests changed, record whether TG001-TG005 checks were run and what they
reported.

When governance is active, record governance-level validation commands, profile,
ADR references, and evidence paths that informed the gate decision.

## done_verification_note

Confirm whether the sprint definition of done is fully satisfied.

Minimum questions to answer:

1. Is the planned functionality implemented?
2. Are there any known in-scope errors still open?
3. Are the required project quality gates green, including TG001-TG005 checks
   when tests changed?
4. Are the relevant docs and synchronized artifacts updated or explicitly unchanged?
5. Is the validation evidence recorded?
6. Is `decision-log.md` current, and was `rollup.md` updated or explicitly left unchanged when warranted?

## handoff_note

1. Replace with what finished.
2. Replace with what remains open.
3. Replace with the next recommended action.
4. Replace with what the next sprint should read first.

## follow_up_note

Record any requested or declined follow-up work.

For the final audit sprint, answer at minimum:

1. Was the user asked whether they want follow-up audits or refactors?
2. Which follow-up items were requested, if any?
3. Which follow-up items were explicitly declined, if any?
4. Did the final validation and documentation synchronization checks pass?
5. Are any governance exceptions, ADR waivers, or follow-up validation items
   still open?

## post_execution_summary_note

Replace with the user-facing post-execution summary that should be recoverable
from this closeout.

When the active mode surfaces post-execution reporting, include at minimum:

1. what changed
2. why it mattered
3. assumptions made
4. considerations moving forward
5. things to watch before the next sprint begins
