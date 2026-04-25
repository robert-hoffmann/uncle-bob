# UB Workflow Deep Dive

`ub-workflow` decides how much structure a piece of work needs. Its core rule
is simple: choose the smallest safe planning lane, then make durable artifacts
the source of truth when the work outgrows chat.

## Lane Choice

```mermaid
flowchart TD
  Start["New request"] --> Small{"Can this be done safely without a durable artifact?"}
  Small -->|Yes| Direct["Direct bounded work"]
  Small -->|No| Bounded{"Is the work bounded but planning-heavy?"}
  Bounded -->|Yes| Spec["Lightweight spec"]
  Bounded -->|No| Initiative["Initiative"]
  Spec --> Promote{"Now needs PRD-level decomposition, sequencing, or staged delivery?"}
  Promote -->|Yes| Initiative
  Promote -->|No| ExecuteSpec["Execute from spec next action"]
  Direct --> Done["Finish with validation and summary"]
  Initiative --> Roadmap["PRD, roadmap, prepared sprints, closeout, final audit"]
```

## The Three Lanes

`Direct bounded work`
- Best for: small, clear tasks.
- Artifact expectation: none beyond normal validation and reporting.
- Risk: staying direct after the work becomes planning-heavy.

`Lightweight spec`
- Best for: bounded work that needs assumptions, scope, options, validation,
  and a next action recorded.
- Artifact expectation: one `spec.md` in the target project’s workflow root.
- Risk: promoting too late after staged execution is already obvious.

`Initiative`
- Best for: multi-session, risky, cross-cutting, or dependency-heavy work.
- Artifact expectation: PRD, roadmap, prepared sprint docs, closeouts, final
  audit, and retained note.
- Risk: using initiative machinery for work that only needed a lightweight
  spec.

## Interaction Modes

Mode changes how visible and interruptive the workflow feels. It does not
weaken readiness rules.

```mermaid
flowchart LR
  Mode["Interaction mode"] --> Reviewed["reviewed: preview, approval, report, pause"]
  Mode --> Flow["flow: short preview, report, manual advancement"]
  Mode --> Auto["auto: concise reports, continue unless interrupted"]
  Mode --> Continuous["continuous/yolo: no routine pause, stop on major blockers"]
  Reviewed --> SameRules["Same gates and validation"]
  Flow --> SameRules
  Auto --> SameRules
  Continuous --> SameRules
```

## Reviewed Mode Matters

In reviewed mode, a request like “start the next sprint” opens the preview. It
does not start implementation. Execution starts only after a later approval
message.

The preview should explain:

1. what repo or project truth says
2. what the agent infers
3. realistic implementation paths
4. the recommended path
5. any questions that change the sprint path
6. the approval boundary

## Initiative Lifecycle

```mermaid
flowchart TD
  Classify["Classify work"] --> Lane["Choose initiative lane"]
  Lane --> Research["Research and discovery"]
  Research --> PRD{"prd_ready?"}
  PRD -->|pass| Roadmap["Generate roadmap"]
  Roadmap --> RoadmapReview{"roadmap_ready human approval?"}
  RoadmapReview -->|pass| SprintPrep["Prepare sprint content"]
  SprintPrep --> SprintReady{"sprint_content_ready?"}
  SprintReady -->|pass| StartGate{"sprint_start_ready when needed?"}
  StartGate -->|pass| Execute["Execute active sprint"]
  Execute --> Closeout{"sprint_closeout?"}
  Closeout -->|pass| More{"More sprints?"}
  More -->|Yes| StartGate
  More -->|No| Audit["Final audit"]
  Audit --> Retained["Write retained note"]
  Retained --> ArchiveReview{"archive_ready human review?"}
  ArchiveReview -->|pass| Complete["initiative_complete"]

  classDef human fill:#fff3bf,stroke:#b7791f,color:#3d2b00;
  class RoadmapReview,ArchiveReview human;
```

## What To Remember

- Chat history is not the system of record.
- Lightweight specs are a real lane, not a weak initiative.
- Roadmap approval is a human checkpoint.
- Prepared sprint files are not the same thing as started execution.
- Every initiative ends with final audit, retained note, and review before
  archive.
