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

## 4) Red-Green-Refactor Loop

### RED

1. add one failing behavior test for the increment
2. run narrow test command
3. confirm intended failure
4. run strict test-signal check for touched test file

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

## 5) Required Checkpoints

Pause at:

1. increment-list approval before cycle start
2. RED confirmation per increment
3. anomalies or strict-gate violations without active bounded exception

## 6) Increment Closure

Record per increment:

1. tests added/updated
2. production code added/updated
3. refactor summary (or `none`)
4. final pass/fail state
