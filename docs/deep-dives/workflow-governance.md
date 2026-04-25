# Workflow And Governance Together

`ub-workflow` and `ub-governance` are adjacent systems. Workflow answers
whether the work package is ready to progress. Governance answers whether the
evidence, risk handling, exception, or decision record is strong enough.

## Separation Of Concerns

```mermaid
flowchart TD
  Request["Work request"] --> Workflow["ub-workflow: lane and execution structure"]
  Request --> Governance["ub-governance: evidence and control depth"]
  Workflow --> WGate["Workflow gates: research, PRD, roadmap, sprint, closeout, archive"]
  Governance --> GGate["Governance gates: pass, fail, blocked"]
  WGate --> Delivery["Delivery decision"]
  GGate --> Delivery
```

## Typical Combinations

`Ordinary planned work`
- `ub-workflow` chooses the lane and artifacts.
- `ub-governance` stays lean or inactive unless a risk question appears.

`High-risk initiative`
- `ub-workflow` owns PRD, roadmap, sprint flow, closeout, and final audit.
- `ub-governance` may add Level 2 evidence, ADR alignment, or claim checks.

`Testing posture review`
- `ub-workflow` may be unnecessary if the task is only review.
- `ub-governance` uses testing mode to assess signal quality.

## Bridge Levels

```mermaid
flowchart LR
  L0["Level 0: no governance bridge"] --> L1["Level 1: light bridge"]
  L1 --> L2["Level 2: full governance coordination"]
  L0 --> Use0["Normal workflow only"]
  L1 --> Use1["Workflow artifacts plus light governance notes"]
  L2 --> Use2["Evidence, ADR, claims, or formal gate alignment"]
```

## Practical Rule

Start with workflow when the problem is delivery shape. Start with governance
when the problem is evidence, test signal, exception handling, or decision
durability. Use both when delivery and control depth are both material.
