# Testing Policy and Signals

This file is the canonical testing policy source for the repository's testing
signal model.

Use descriptive names in normal guidance.
Keep `TG001` through `TG005` as stable internal IDs for tooling and backward
compatibility.

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

1. `Type Redundancy` (`TG001`): runtime tests that restate type-system
    guarantees
2. `Interaction Without Outcome` (`TG002`): interaction assertions without
    observable outcome assertions
3. `Pass-Through Test` (`TG003`): trivial getter/setter pass-through tests
4. `Happy-Path-Only Suite` (`TG004`): suite-level happy-path concentration
    with no boundary/error representation

### Warning rule

1. `Internal-Detail Bias` (`TG005`): probable internal-detail verification
    bias

### Short Examples

`Interaction Without Outcome` (`TG002`) should read like this in practice:

```ts
// Avoid: interaction-only assertion
it('saves the order', async () => {
    await saveOrder(order)
    expect(apiClient.post).toHaveBeenCalledWith('/orders', order)
})

// Better: pair the boundary interaction with observable outcome
it('saves the order and returns the created id', async () => {
    apiClient.post.mockResolvedValue({ id: 'ord-123' })
    await expect(saveOrder(order)).resolves.toEqual({ id: 'ord-123' })
    expect(apiClient.post).toHaveBeenCalledWith('/orders', order)
})
```

`Type Redundancy` (`TG001`) should avoid runtime tests that only restate type
contracts:

```ts
// Avoid: re-checking a static type guarantee at runtime
it('returns a string id', () => {
    expect(typeof buildOrderId()).toBe('string')
})
```

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

Portable script surface:

```bash
uv run python .agents/skills/ub-governance/scripts/check_test_signal.py --path <test-file-or-dir> --language auto --strict
```

Replace `uv run python` with the host repository's configured Python runner,
such as `python`, when `uv` is unavailable or inappropriate for the host.

For JSON output, the portable script surface is:

```bash
uv run python .agents/skills/ub-governance/scripts/check_test_signal.py --path <test-file-or-dir> --language auto --format json --strict
```

## 7) Flake Policy

1. isolate flaky tests in visible quarantine
2. assign owner and fix ETA
3. do not accept net-new flaky tests without a bounded exception

## 8) Safety Notes

Agent testing runs should use command/path/network allowlists and avoid production secrets.
