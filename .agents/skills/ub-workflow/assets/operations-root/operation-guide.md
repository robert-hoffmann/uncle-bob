# Initiative Operation Guide

<!-- #region Purpose And Use -->
## Purpose

This document defines a strict, reusable standard operating procedure for large
or risky initiatives that cannot be executed reliably from chat history alone.

Use this SOP when work requires:

1. planning and R&D before implementation
2. a self-contained PRD that can be executed later
3. multiple stop-and-resume execution sprints
4. deterministic evidence and explicit gate states
5. a durable retained summary after completion

This SOP is written to be usable by a PM, an engineer, and an AI agent with the
same source of truth.

## Typical Ownership Model

The most common workflow is:

1. a human authors the initial PRD
2. a human or AI agent scaffolds a dated initiative root and copies that PRD into `./prd.md`
3. a human or AI agent refines the PRD and produces a durable `roadmap.md`
4. the human reviews and explicitly approves the roadmap
5. sprint-pack preparation happens only after the roadmap is approved
6. sprint folders are initialized only after the roadmap is approved when directory materialization is needed
7. the workflow stops until the human explicitly requests the active sprint
8. execution happens one sprint at a time, with a human review checkpoint after each sprint, until the initiative is complete

This SOP supports other authorship patterns, but it assumes the initial product
or engineering intent has a clear human owner.

## When To Use This SOP

Use this SOP for work that has at least one of these properties:

1. spans more than one working session
2. changes behavior, architecture, or operating model
3. needs explicit option analysis or governance review
4. needs evidence-backed handoffs between sprints
5. must be resumable without relying on prior chat context

Do not use this SOP for small, single-session fixes where a lightweight task
note is enough.

Before starting this SOP, make a scale decision:

1. direct bounded task when no durable planning artifact is needed
2. lightweight spec under `./specs/YYYY-MM-DD-slug/spec.md` when the work
   needs a written contract but not a roadmap and sprint pack
3. initiative under `./initiatives/YYYY-MM-DD-slug/` when the work needs a
   PRD, roadmap, and resumable sprint execution

## Non-Negotiable Rules

1. One initiative uses one initiative root directory.
2. The PRD must be self-contained and execution-ready before sprinting starts.
3. Every sprint must be stop-resume safe.
4. Evidence, planning, and closeout are separate artifacts.
5. Gate states are always `pass`, `fail`, or `blocked`.
6. Exceptions must be explicit, temporary, and owned.
7. The retained note is the durable record after completion.
8. Chat history is never the system of record.
<!-- #endregion Purpose And Use -->

<!-- #region Operating Model -->
## Operating Model

This SOP defines a six-phase lifecycle.

### Phase 1: Plan And Author The PRD

Goal: turn research and intent into one self-contained PRD that is ready to be
executed later by a different operator or agent.

### Phase 2: Plan And Approve The Roadmap

Goal: turn the approved PRD into one durable roadmap that can initialize sprint
folders without relying on chat history.

### Phase 3: Prepare The Sprint Pack

Goal: turn the approved roadmap into execution-ready sprint PRDs before any
implementation begins.

### Phase 4: Initialize Sprint Directories

Goal: materialize or repair sprint directories without conflating scaffolding
with sprint execution.

### Phase 5: Execute In Ordered Sprints

Goal: split the PRD into bounded sprints that can be paused, resumed, audited,
and handed off without loss of context.

### Phase 6: Final Audit And Durable Retention

Goal: finish the roadmap with a mandatory final audit, confirm completeness and
synchronization, ask for any follow-up audits or refactors, then replace bulky
temporary execution detail with a concise retained note.

## Lifecycle Gates

This SOP uses lifecycle gates in addition to any repository-specific merge or
release gates.

| Gate | Meaning | Allowed States |
| ---- | ------- | -------------- |
| `prd_ready` | The PRD is execution-ready and sprint planning may begin | `pass`, `fail`, `blocked` |
| `roadmap_ready` | The roadmap is execution-ready and sprint preparation may begin | `pass`, `fail`, `blocked` |
| `sprint_content_ready` | The sprint pack is execution-ready and sprint start readiness may begin | `pass`, `fail`, `blocked` |
| `sprint_start_ready` | The next sprint may begin after context refresh and any required reviewed-mode approval | `pass`, `fail`, `blocked` |
| `sprint_closeout` | A sprint has enough evidence and handoff detail to pause or continue | `pass`, `fail`, `blocked` |
| `archive_ready` | The final audit output is ready for explicit archive review | `pass`, `fail`, `blocked` |
| `initiative_complete` | The initiative has a retained note and a validated completion baseline | `pass`, `fail`, `blocked` |

`roadmap_ready: pass` is human-owned in this workflow. The agent may recommend
approval after surfacing the roadmap review checklist, but the human must
explicitly approve the roadmap before that gate is set.

State intent:

- `pass`: required controls are satisfied
- `fail`: the work was evaluated and one or more required controls failed
- `blocked`: required controls cannot be satisfied yet because prerequisites,
  evidence, or approvals are missing
<!-- #endregion Operating Model -->

<!-- #region Canonical Layout -->
## Canonical Directory Layout

Store every initiative or lightweight spec under one canonical root.

## Path Portability Rules

Write all operational instructions relative to the current operations root when
possible.

Preferred path style inside this SOP and inside initiative files:

1. from this initiative index, use `./<yyyy-mm-dd>-<slug>/...`
2. from an initiative root, use `./prd.md`, `./sprints/`, `./retained-note.md`
3. use repo-root-relative paths only when referencing legacy material outside
  the current operations root

Generic pattern:

```text
<operations-root>/
  archive/
  initiatives/
    AGENTS.md
    README.md
    operation-guide.md
    user-guide.md
    <yyyy-mm-dd>-<initiative-slug>/
      AGENTS.md
      README.md
      prd.md
      roadmap.md
      research/
      sprints/
        01-<sprint-slug>/
          sprint.md
          closeout.md
          evidence/
        ./
          2026-03-27-example-initiative/
      exceptions/
      retained-note.md
  specs/
    <yyyy-mm-dd>-<spec-slug>/
      spec.md
```

The generated operations root does not need a checked-in `initiative-template/`
copy. The scaffold helper uses the skill's internal canonical templates to
create initiative roots and sprint skeletons on demand.

## Directory Contract

### `README.md`

The operator-facing status file for the initiative root.

Use it as the root summary and entry point.

`roadmap.md` is the smaller live progress document.

### `prd.md`

The self-contained initiative definition. It must remain understandable without
opening research or sprint files.

### `research/`

Optional source captures, exploratory notes, and supporting material from the
planning phase. The PRD may cite it, but must not depend on it for core intent.

### `sprints/`

The execution packs. Each sprint gets its own numbered directory so planning,
evidence, and closeout stay co-located.

Use the canonical `ub-workflow` sprint template when initializing all sprint
directories from the master roadmap. Do not initialize sprint directories until
`roadmap_ready: pass`.
Initialization prepares execution; it does not start sprint work automatically.

### `exceptions/`

Optional explicit exception records. If no exceptions are active, this folder
may be omitted.

### `retained-note.md`

The durable completion record for the initiative.

### `specs/`

Optional lightweight planning roots for work that is bigger than a direct task
but smaller than a full initiative.

## Naming Rules

1. Initiative roots use `YYYY-MM-DD-slug`.
2. Sprint directories use `NN-slug` with zero-padded ordering.
3. Evidence directories live inside the owning sprint directory.
4. Singular control files keep fixed names: `README.md`, `AGENTS.md`, `prd.md`,
   `roadmap.md`, `retained-note.md`, `sprint.md`, and `closeout.md`.
5. Do not scatter PRDs, evidence, and retained notes across unrelated folders.
6. Prefer relative paths inside operation artifacts unless cross-root references
  are necessary.
<!-- #endregion Canonical Layout -->
