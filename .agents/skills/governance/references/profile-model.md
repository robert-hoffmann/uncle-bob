# Profile Model

Use this model to choose governance strictness.

## 1) Profiles

| Profile | Default Use | Intent |
| ------- | ----------- | ------ |
| `lean` | small to medium projects | minimum deterministic controls with low process overhead |
| `advanced` | complex or high-risk projects | expanded controls for risk, scale, and audit depth |

## 2) Lean Defaults

Lean profile enables:

1. deterministic merge gate
2. explicit owner/expiry/follow-up on exceptions
3. focused artifact set for changed scope
4. minimal required reporting sections

Lean profile does not require:

1. broad standards mapping matrices
2. non-critical exhaustive gate artifacts
3. migration parity overlays unless migration is in scope

## 3) Advanced Activation

Enable `advanced` profile when any of these are true:

1. regulated or high-impact domain
2. high-risk path changes are frequent
3. release-critical multi-service coupling
4. explicit customer or compliance requirement

Advanced profile may add:

1. expanded confidence gates
2. stronger decision-memory controls
3. broader artifact retention and audit depth
4. additional non-functional checks

## 4) Selection Rule

- Use `lean` by default.
- Escalate to `advanced` only with explicit rationale.
