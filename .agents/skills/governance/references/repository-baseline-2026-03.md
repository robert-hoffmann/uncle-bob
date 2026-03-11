# Repository Baseline 2026-03

This baseline is date-stamped to `2026-03-04` and optimized for small to medium projects.

## 1) Lean Default Matrix

| Area | Lean Default | Notes |
| --- | --- | --- |
| Node runtime | Active LTS (Node 20+) | Keep policy explicit if pinned |
| Python runtime | Python 3.11+ | Keep `requires-python` explicit |
| Tooling policy | one package manager, one formatter, one lint entrypoint | Keep lockfile authoritative |
| CI merge gate | lint + typecheck + tests + build | deterministic and reproducible |
| Security baseline | dependency governance + secret scanning | least-privilege workflows |
| Release baseline | `release-please` + Conventional Commits | minimal release ops overhead |

## 2) Required Artifacts

1. `.editorconfig`
2. `.gitignore`
3. `.gitattributes`
4. `README.md`
5. `CONTRIBUTING.md`
6. `SECURITY.md`
7. `LICENSE`
8. `.env.example`
9. CI workflows under `.github/workflows/`
10. lockfiles for active ecosystems

## 3) Advanced Add-ons (Opt-In)

Enable only when explicitly needed:

1. stronger branch/ruleset restrictions
2. extended non-functional gates in PR flows
3. provenance/attestation requirements for release-critical artifacts
4. expanded audit retention or compliance mapping

## 4) Determinism Rules

1. lockfiles are mandatory for active ecosystems
2. CI install mode must remain reproducible
3. build/test commands must be documented and reproducible

## 5) Exception Handling

Use `references/exception-contract.md`.
No local exception schema definitions are allowed in this skill.
