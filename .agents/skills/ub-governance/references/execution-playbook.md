# Execution Playbook (Agentic TDD)

Use this playbook for behavior-changing work delivered with semi-autonomous Red-Green-Refactor.

## 1) Intake and Scope

1. capture feature objective in one sentence
2. capture acceptance boundaries (expected outcomes, boundary/error conditions, non-goals)
3. detect active test command from repository truth

## 2) Runner Detection (Repo-Truth-First)

Resolution order:

1. project task scripts
2. CI/test config commands
3. language defaults
4. user confirmation only if still ambiguous

## 3) Increment Design

Default order:

1. degenerate behavior (`empty`, `none`, `zero`, no-op)
2. boundary/error behavior
3. minimal happy path
4. additional valid variants
5. integration composition

Avoid anti-patterns:

1. happy-path-only increment sets
2. type-system-restatement tests
3. internal call-order verification without outcome assertions
4. giant mixed-behavior increments

Test readability note:

1. prefer DAMP over DRY in tests when a small amount of duplication makes each
   scenario easier to read independently
2. avoid helper abstraction that hides setup, trigger, or observed outcome
3. prefer two explicit tests over one parameterized blur when the scenarios
   exercise meaningfully different behavior

## 4) Red-Green-Refactor Loop

### RED

1. add one failing behavior test for the increment
2. run narrow test command
3. confirm intended failure
4. run strict test-signal check for touched test file
5. confirm RED realism before implementation

RED realism is invalid when:

1. the implementation under review is mocked or replaced
2. the mocked response encodes the expected answer
3. the assertion only checks calls, call count, or call order
4. the test would still pass if the real implementation were deleted
5. the assertion is snapshot-only, render-only, coverage-only, or
   does-not-throw-only
6. a bugfix regression test does not exercise the real reported defect path

For reported defects, the regression test must exercise the real defect path
unless a bounded test-double exception exists. Keep any RED realism note short:
behavior under test, public surface exercised, why it fails without the fix,
and test doubles used.

### GREEN

1. implement minimal code for RED
2. rerun narrow test command
3. rerun full-scope project tests
4. stop and resolve unrelated failures before continuing

### REFACTOR

1. refactor for clarity/duplication reduction only
2. keep behavior unchanged
3. rerun full-scope tests
4. revert/fix immediately if regressions appear

### Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "I already know the bug; I can fix it first" | Regression-first reproduction is the proof that the defect path exists and stays fixed. |
| "These cases are basically the same" | Merge scenarios only when the observable outcome is truly the same; otherwise keep the tests distinct and readable. |
| "I will run the strict test-signal check later" | Running it during RED prevents low-signal tests from compounding across increments. |
| "The full suite is enough" | Narrow checks prove increment intent; broader checks prove regression safety. Both matter. |
| "The mock proves the scenario" | A double can support setup, but it cannot be the proof for behavior it replaced. |

## 5) Required Checkpoints

Pause at:

1. increment-list approval before cycle start
2. RED confirmation per increment
3. anomalies or strict-gate violations without active bounded exception
4. repeated rationalization pressure that is pushing the work away from
   behavior-first, outcome-based checks

## 6) Increment Closure

Record per increment:

1. tests added/updated
2. production code added/updated
3. refactor summary (or `none`)
4. RED realism note when a test double affects the proof
5. final pass/fail state
