# CI Artifact Contract (Testing)

This file defines testing-specific artifacts for blocking gates.

## 1) Required Merge-Gate Testing Artifacts

1. JUnit XML outputs for test runners used
2. coverage outputs (`lcov`/`xml`/`html` as appropriate)
3. E2E report outputs when E2E is in merge scope
4. command log summary for reproducibility
5. strict test-signal report when TG checks run

Suggested paths:

```text
artifacts/
  junit/
  coverage/
  e2e-report/
  traces/
  test-signal-gates.json
  command-log.txt
```

## 2) Confidence/Release Testing Expansion

When profile/scope requires expanded gates:

1. full integration suite outputs
2. full contract verification outputs
3. full e2e regression outputs
4. non-functional checks (accessibility/performance/security) when in scope

## 3) Enforcement

1. TG001-TG004 are blocking
2. TG005 is warning-only
3. overrides require active bounded exception metadata from governance contract

