# UB Initiative Flow Roadmap

## Purpose

This document tracks deferred work for `ub-initiative-flow` after the initial
skill, references, scaffold assets, and companion agent are in place.

Use it as the durable pickup surface for future enhancement work.

## Current Release Scope

The initial release includes:

1. the core skill contract
2. reusable references
3. neutral initiative scaffolding assets
4. a companion pilot agent
5. a deterministic scaffold helper

The initial release still does not include plugin packaging, hooks, or deep
governance automation.

## Product Summary

`ub-initiative-flow` gives teams a portable operating model for larger work:
discovery, self-contained PRD, full roadmap, standalone resumable sprints,
final audit, and retained note.

The skill is intentionally process-opinionated and repository-neutral.

## Goals

1. keep large initiatives stop-resume safe
2. make PRDs executable by a developer, PM, or agent
3. initialize sprint structure consistently across repositories
4. keep final-audit and retained-memory discipline explicit
5. coordinate cleanly with `ub-quality` and `ub-governance`

## Non-Goals

1. replace ub-governance
2. require ADR or claim systems in every repository
3. auto-solve roadmap decomposition from arbitrary vague prompts
4. package the workflow as a plugin in the first release

## Completed Since Initial Release Plan

### Phase 01: Deterministic Scaffold Helper

Status:
Implemented.

Delivered behavior:

1. copies the initiative template into a new target root
2. fills core placeholders from arguments or defaults
3. preserves unresolved optional placeholders when values are omitted
4. blocks reruns against populated targets to avoid clobbering work

### Phase 02: Agent UX Refinement

Status:
Implemented.

Delivered behavior:

1. the agent now exposes scaffold, resume, and what-next as direct handoff paths
2. argument hints cover the main initiative phases and recovery cases
3. the agent includes orientation, routing, and workflow-recovery guidance
4. `docs/user-guide.md` now provides usage examples and smoke prompts for later iteration

## Deferred Roadmap

### Phase 03: Governance-Integrated Planning

Objective:
Expand the governance bridge into first-class planning prompts for evidence
level, profile selection, and validation mapping.

Why deferred:
The portable lean core should prove useful before deeper governance coupling is
added.

Definition of done:

1. governance bridge prompts are explicit and optional
2. repos using ub-governance can declare profile and validation depth at setup
3. final audit templates map cleanly to governance expectations

### Phase 04: Smarter Roadmap and Sprint Generation

Objective:
Improve the workflow for turning a finished PRD into a high-quality ordered
roadmap and better standalone sprint packs.

Why deferred:
The current release ships the contract and structure first; smarter decomposition
should follow real usage feedback.

Definition of done:

1. roadmap generation heuristics are documented
2. sprint planning guidance handles dependencies and validation focus better
3. anti-pattern checks catch overlarge or non-standalone sprints

### Phase 05: Hooks and Lifecycle Automation

Objective:
Add carefully scoped hooks only where deterministic lifecycle help materially
improves reliability.

Why deferred:
Hooks increase complexity and should follow proven workflow pain points.

Definition of done:

1. hook candidates are narrowly scoped and justified
2. hook behavior is reviewable and safe
3. the workflow still works without hooks

### Phase 06: Plugin and Cross-Repo Distribution

Objective:
Package the initiative workflow for broader internal reuse if distribution needs
outgrow repository-local skills and agents.

Why deferred:
Packaging should follow proven local adoption.

Definition of done:

1. the bundle structure is stable enough to distribute
2. plugin packaging or equivalent distribution is documented
3. portability notes cover repo-local adaptation expectations

## Resume Guidance

When resuming work on this skill, read in this order:

1. this `roadmap.md`
2. `SKILL.md`
3. `references/workflow-contract.md`
4. `references/artifact-contracts.md`
5. the scaffold assets under `assets/initiative-template/`
6. `.github/agents/ub-initiative-flow.agent.md`