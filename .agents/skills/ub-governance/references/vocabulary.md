# Vocabulary

Use these terms consistently across governance outputs.

## 1) Core Terms

- `merge gate`: PR-time blocking validation
- `confidence gate`: scheduled/pre-release blocking validation
- `release gate`: release-readiness blocking validation
- `deterministic check`: reproducible check from clean checkout
- `high-risk path`: path pattern that requires stronger decision controls
- `decision-memory`: durable architecture decision traceability
- `claim-verification`: confidence status for policy claims
- `policy drift`: divergence from declared governance policy

## 2) Status Terms

- `pass`: required controls satisfied
- `fail`: executed controls failed
- `blocked`: gate cannot exit due to unmet prerequisites

## 3) Exception Terms

- `active`: exception is unexpired and in use
- `expired`: exception date passed and no renewal is active
- `renewed`: new bounded record replaces prior exception
- `resolved`: exception no longer needed
