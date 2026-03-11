# Evidence Lifecycle

## 1) Evidence Root

Define one evidence root directory (for example `docs/evidence/` or `evidence/`).

## 2) Folder Layout

```text
<evidence-root>/
|- phase-01/
|- phase-02/
|- phase-NN/
`- agent-ops/
```

Phase folders hold run-specific artifacts.
`agent-ops/` holds cross-cutting governance records.

## 3) Phase Folder Contents

1. command logs
2. test/build/contract outputs
3. decision logs with artifact references
4. release checklists for release-scoped gates

## 4) Agent-Ops Contents

1. `agent-validation-records.md`
2. `policy-exceptions.md`
3. `tooling-baseline.md`

## 5) Decision-Memory Root

Canonical decision files live in `docs/adr/`:

1. `docs/adr/index.md`
2. `docs/adr/registry.json`
3. `docs/adr/claim-register.json`

## 6) Freshness and Reproducibility

1. blocking artifacts must map to current evaluated revision
2. stale artifacts must be re-generated or explicitly excepted
3. deterministic reruns must reproduce blocking artifact outputs

## 7) Anti-Patterns

1. scattered evidence outside the declared evidence root
2. orphaned artifacts without gate linkage
3. stale pass-through evidence used for new gate decisions
4. decision/claim drift without explicit remediation
