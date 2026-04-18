# Testing Policy and Signals

This file is the canonical testing policy source for TG001-TG005.

## 1) Policy Intent

1. keep test feedback high-signal and deterministic
2. prioritize externally observable behavior over internals
3. keep exceptions explicit, bounded, and owned

## 2) TDD Default

For behavior-changing work:

1. write/update failing behavior test
2. implement minimal passing code
3. refactor while tests stay green

For reported defects, apply the `Prove-It` pattern:

1. reproduce the reported defect with a failing regression test first
2. confirm the failing test matches the intended defect path
3. implement the smallest fix that makes the regression test pass
4. rerun narrow and broader validation so the fix is proven, not inferred

Use governance exception metadata if TDD-first is temporarily bypassed.

## 3) Strict Test-Signal Rules

### Blocking rules

1. `TG001`: runtime tests that restate type-system guarantees
2. `TG002`: interaction assertions without observable outcome assertions
3. `TG003`: trivial getter/setter pass-through tests
4. `TG004`: suite-level happy-path concentration with no boundary/error representation

### Warning rule

1. `TG005`: probable internal-detail verification bias

## 4) Allowed Test Patterns

1. assert public behavior and outcomes
2. cover boundary/error behavior early
3. use mocks only at inaccessible boundaries and pair with outcome assertions

When RED-first discipline starts to erode under delivery pressure, use the
execution playbook's rationalization checks before continuing with the next
increment.

## 5) Suite-Balance Guidance

1. keep most tests fast and local to the behavior being changed
2. add boundary or integration checks when behavior crosses storage, process,
   file, or network boundaries
3. keep a smaller set of broad-flow tests for critical end-to-end behavior
4. treat this as risk-based balance guidance, not as a fixed quota model

## 6) Deterministic Gate Command

Use:

```bash
python .agents/skills/ub-governance/scripts/check_test_signal.py --path <test-file-or-dir> --language auto --strict
```

For JSON output:

```bash
python .agents/skills/ub-governance/scripts/check_test_signal.py --path <test-file-or-dir> --language auto --format json --strict
```

## 7) Flake Policy

1. isolate flaky tests in visible quarantine
2. assign owner and fix ETA
3. do not accept net-new flaky tests without a bounded exception

## 8) Safety Notes

Agent testing runs should use command/path/network allowlists and avoid production secrets.
