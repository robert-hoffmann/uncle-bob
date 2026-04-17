# Sprint 01 Evidence

## Before And After Lifecycle Summary

Before Sprint 01, `ub-workflow` compressed the lifecycle to discovery, PRD,
roadmap, sprint initialization, sprint execution, final audit, and retained
note. That model left one critical gap: it did not recognize sprint-content
preparation as a first-class phase, so an initiative could have a rich roadmap
but still end up with placeholder-only `sprint.md` files.

After Sprint 01, the lifecycle is explicitly:

1. research and discovery
2. PRD authoring and readiness
3. initiative scaffold and baseline setup
4. roadmap generation and approval
5. sprint-content preparation
6. sprint materialization and start readiness
7. ordered sprint execution
8. sprint closeout and review pause
9. final audit and review pause
10. retained note and archive decision

The practical change is that roadmap approval no longer implies execution
readiness by itself. Sprint content must be prepared, written down, and
reviewable before any sprint begins.

## Gate Glossary

- `research_ready`: discovery is grounded enough to support a durable PRD
- `prd_ready`: the PRD is execution-ready and roadmap work can start
- `roadmap_ready`: the roadmap is execution-ready and approved for downstream
  work
- `sprint_content_ready`: the sprint pack has execution-ready sprint PRDs
- `sprint_start_ready`: the next sprint can begin after any needed context
  refresh
- `sprint_closeout`: the active sprint is safe to pause, hand off, or close
- `archive_ready`: final audit output is ready for explicit archive review
- `initiative_complete`: the initiative has completed final audit and retained
  note

## Ownership Notes

- `roadmap_ready` remains a human-owned review checkpoint.
- `archive_ready` remains a human-owned review checkpoint.
- The other gates are shared workflow gates that can be evaluated by the
  operator or agent, but their rationale must be written into initiative
  artifacts.
