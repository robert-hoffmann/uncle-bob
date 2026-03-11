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

## 5) Deterministic Gate Command

Use:

```bash
python .agents/skills/governance/scripts/check_test_signal.py --path <test-file-or-dir> --language auto --strict
```

For JSON output:

```bash
python .agents/skills/governance/scripts/check_test_signal.py --path <test-file-or-dir> --language auto --format json --strict
```

## 6) Flake Policy

1. isolate flaky tests in visible quarantine
2. assign owner and fix ETA
3. do not accept net-new flaky tests without a bounded exception

## 7) Safety Notes

Agent testing runs should use command/path/network allowlists and avoid production secrets.

