# Gate and Report Contract

This file defines shared gate semantics and shared governance report sections.

## 1) Canonical Gate Types

| Gate | Trigger | Blocking |
|---|---|---|
| `merge` | pull request validation | yes |
| `confidence` | scheduled or pre-release validation | yes |
| `release` | release readiness validation | yes |

## 2) Canonical Gate States

Allowed states:

1. `pass`
2. `fail`
3. `blocked`

State intent:

- `pass`: required controls satisfied
- `fail`: control execution completed with one or more failed checks
- `blocked`: required controls cannot be satisfied yet due to missing prerequisites, stale artifacts, or expired exceptions

## 3) Shared Report Sections

All governance reports should include:

1. `environment_note`: stack and runtime context
2. `scope_note`: evaluated scope and profile (`lean` or `advanced`)
3. `decision_note`: chosen path and one alternative with concise pros/cons
4. `gate_note`: gate type and result (`pass|fail|blocked`)
5. `exception_note`: active exceptions or explicit `none`
6. `validation_note`: commands/checks executed and outcomes

## 4) Domain Extensions

Domain skills may append domain-specific report sections.
They must not redefine the canonical sections above.
