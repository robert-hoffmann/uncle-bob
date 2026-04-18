# Evidence Lifecycle

## 1) Evidence Root

Define one evidence root directory (for example `docs/evidence/` or `evidence/`).

For workflow-backed initiatives, the default operational evidence root is
sprint-local rather than initiative-global: each sprint's `./evidence/` folder
holds the direct evidence for that sprint.

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

Workflow-backed initiative pattern:

```text
<initiative-root>/
|- research/
|- exceptions/
|- rollup.md
|- sprints/
|  |- 01-.../
|  |  |- decision-log.md
|  |  `- evidence/
|  |- 02-.../
|  |  |- decision-log.md
|  |  `- evidence/
|  `- NN-.../
|     |- decision-log.md
|     `- evidence/
`- retained-note.md
```

Intent:

1. sprint `evidence/` stores raw sprint-scoped proof close to the work
2. sprint `decision-log.md` stores the running sprint-scoped decision memory
3. `rollup.md` aggregates the readable cross-sprint summary, but it does not
   replace sprint-local evidence as the source of truth
4. `research/` stays supportive and pre-decision in character
5. `exceptions/` stays bounded and explicit rather than becoming a generic note
   store

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

Canonical repository ADR files live in `docs/adr/` when ADR escalation applies:

1. `docs/adr/index.md`
2. `docs/adr/registry.json`
3. `docs/adr/claim-register.json`

For Level 1 workflow-backed work, decision memory normally lives first in the
approved workflow artifacts and sprint-local evidence, not in repository ADRs
by default.

## 6) Freshness and Reproducibility

1. blocking artifacts must map to current evaluated revision
2. stale artifacts must be re-generated or explicitly excepted
3. deterministic reruns must reproduce blocking artifact outputs

## 7) Anti-Patterns

1. scattered evidence outside the declared evidence root
2. orphaned artifacts without gate linkage
3. stale pass-through evidence used for new gate decisions
4. decision/claim drift without explicit remediation
5. escalating routine sprint decisions into repository ADRs when workflow
   artifacts already provide sufficient durable context
6. using `research/` or `exceptions/` as a default diary when `decision-log.md`
   or `rollup.md` should hold the workflow memory instead
