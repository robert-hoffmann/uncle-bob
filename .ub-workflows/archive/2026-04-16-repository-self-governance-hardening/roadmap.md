# Sprint Roadmap

Status: complete

This is the small live progress document for the initiative.

This roadmap was generated from `./prd.md` plus the verified planning addendum
recorded on 2026-04-16. After sprint initialization, a workflow gap was
discovered: the sprint pack was scaffolded with placeholder-only sprint PRDs.
The first four sprints below correct `ub-workflow` itself so the original
hardening work can proceed under an execution-ready, resumable sprint model.
Do not start sprint execution until the roadmap is reviewed, explicitly
approved, and the initiative `README.md` records `roadmap_ready: pass`.

## Overall Checklist

- [x] Master PRD imported into `./prd.md`
- [x] Master roadmap generated from `./prd.md`
- [x] Roadmap reviewed and approved with `roadmap_ready: pass`
- [x] All sprint folders initialized under `./sprints/` from `./sprint-template/`
- [x] Sprint execution started
- [x] All sprint closeouts completed
- [x] Final audit completed as the last roadmap item
- [x] Follow-up audit or refactor decision recorded
- [x] `./retained-note.md` written

## Current Position

- Current sprint: `none`
- Last completed sprint: `Final Audit - Repository Hardening Final Audit`
- Next sprint: `none`
- Resume from: `none`
- Active blockers: `none`

## Roadmap Objective

Correct `ub-workflow`'s sprint-preparation and resume model first, then ship a
self-validating repository maintenance baseline that keeps skill inventory,
custom-agent inventory, root instructions, metadata, workflow assets, and
contributor expectations aligned over time while preserving the repository's
existing architecture and low-noise governance posture.

## PRD Scope Summary

In scope:

1. Correct `ub-workflow` so sprint PRDs are prepared as real execution
   artifacts before work begins and the workflow remains resumable after
   session resets.
2. Align authoritative repository surfaces with verified disk truth, including
   removal of `Explore` from published inventory and convergence on
   `AGENTS.md`.
3. Add repository-wide integrity automation for catalog, metadata, path or
   case, and skill-structure validation with local and CI parity.
4. Harden the workflow scaffold and improve packaging clarity plus targeted
   quality uplift for weaker skill surfaces.

Out of scope:

1. Full phase-1 generation of all repository docs from a central manifest.
2. Arbitrary semantic validation of prose outside structured or explicit
   authoritative surfaces.
3. Deep retrofitting of every skill with scripts or tests before the integrity
   baseline proves stable and useful.

## Sprint Sequence

Do not run `init-sprints` until this roadmap is complete, reviewed, and the
initiative `README.md` records `roadmap_ready: pass`.

- [x] Sprint 01 - Lifecycle And Gate Redesign
  - Path: `./sprints/01-lifecycle-and-gate-redesign/sprint.md`
  - Goal: redesign `ub-workflow`'s lifecycle and gate model so sprint
      preparation, review pauses, and archive review are explicit and durable
  - Depends on: `none`
  - Validation focus: lifecycle consistency across contract, skill, and agent;
      explicit gate semantics; and session-reset stop-resume discipline
  - Evidence folder: `./sprints/01-lifecycle-and-gate-redesign/evidence/`
  - Subtasks:
        - [x] Rewrite the workflow contract to include sprint preparation,
         optional context refresh, sprint review pauses, and final archive
         review.
        - [x] Update the skill and companion agent to follow the corrected
         lifecycle and gate model.
        - [x] Make the session-reset assumption explicit so written artifacts, not
         chat history, remain the system of record.

- [x] Sprint 02 - Skill Agent And Reference Alignment
  - Path: `./sprints/02-skill-agent-and-reference-alignment/sprint.md`
  - Goal: propagate the corrected workflow lifecycle into every `ub-workflow`
      contract, guide, and companion-agent surface
  - Depends on: `Sprint 01 - Lifecycle And Gate Redesign`
  - Validation focus: contract alignment, user-guide alignment, and removal of
      placeholder-shell assumptions from workflow-facing docs
  - Evidence folder: `./sprints/02-skill-agent-and-reference-alignment/evidence/`
  - Subtasks:
        - [x] Update the artifact contract so sprint PRDs are execution-ready
         artifacts instead of starter shells.
        - [x] Update validation, scaffold-adaptation, and scaffold-helper
         references so sprint preparation is a distinct phase before
         execution.
        - [x] Update the user guide and broader agent wording so the same
         lifecycle is taught everywhere.

- [x] Sprint 03 - Helper And Template Redesign
  - Path: `./sprints/03-helper-and-template-redesign/sprint.md`
  - Goal: redesign the workflow helper and sprint template so the roadmap can
      become real pre-execution sprint PRDs
  - Depends on: `Sprint 02 - Skill Agent And Reference Alignment`
  - Validation focus: richer roadmap parsing, explicit sprint-preparation
      behavior, and clear separation between machine placeholders and human
      reasoning fields
  - Evidence folder: `./sprints/03-helper-and-template-redesign/evidence/`
  - Subtasks:
        - [x] Redesign `roadmap_sprint_entries()` so it can consume the richer
         sprint metadata already present in the roadmap.
        - [x] Add or model an explicit `prepare-sprints` phase before execution.
        - [x] Redesign the sprint template so roadmap-derived sections and
         human-authored reasoning sections are clearly separated.

- [x] Sprint 04 - Workflow Regression And Resume Scenarios
  - Path: `./sprints/04-workflow-regression-and-resume-scenarios/sprint.md`
  - Goal: protect the corrected workflow lifecycle with regression and
      session-reset resume coverage
  - Depends on: `Sprint 03 - Helper And Template Redesign`
  - Validation focus: gating behavior, prepared sprint coverage,
      session-reset resume order, and final review pauses before archive
  - Evidence folder: `./sprints/04-workflow-regression-and-resume-scenarios/evidence/`
  - Subtasks:
        - [x] Add regression coverage for the rich-roadmap but empty-sprint failure
         mode.
        - [x] Add resume scenarios for later sprints after a session reset.
        - [x] Add final-audit pause and archive-review coverage.

- [x] Sprint 05 - Inventory Alignment And AGENTS Rename
  - Path: `./sprints/05-inventory-alignment-and-agents-rename/sprint.md`
  - Goal: align public inventory surfaces with verified repository truth and
      complete the root-registry filename convergence to `AGENTS.md`
  - Depends on: `Sprint 04 - Workflow Regression And Resume Scenarios`
  - Validation focus: authoritative inventory counts, filename and casing
      correctness, README install-path correctness, and version-metadata
      reconciliation plan
  - Evidence folder: `./sprints/05-inventory-alignment-and-agents-rename/evidence/`
  - Subtasks:
        - [x] Remove `Explore` from published repository agent inventory and
         metadata descriptions while preserving valid built-in subagent
         references in local `.agent.md` files.
        - [x] Rename `AGENTS.MD` to `AGENTS.md` and update all canonical
         references, installation snippets, and validator assumptions.
        - [x] Reconcile version drift across `pyproject.toml`, `plugin.json`, and
         `.github/plugin/marketplace.json`.

- [x] Sprint 06 - Repository Integrity Validators
  - Path: `./sprints/06-repo-integrity-validators/sprint.md`
  - Goal: add the repository-wide integrity baseline under ub-governance using
      the existing direct-CLI validation pattern
  - Depends on: `Sprint 05 - Inventory Alignment And AGENTS Rename`
  - Validation focus: deterministic checker behavior, low-noise authoritative
      scope, exact path validation, and runtime-facing skill reference checks
  - Evidence folder: `./sprints/06-repo-integrity-validators/evidence/`
  - Subtasks:
        - [x] Implement `check_repo_catalog.py` for disk-versus-registry
         comparison across skills, custom agents, README, and root registry
         surfaces.
        - [x] Implement `check_package_metadata.py`, `check_repo_paths.py`, and
         `check_skill_schema.py` using the smallest shared helper surface that
         still keeps CLI execution straightforward.
        - [x] Define the ignore-scope behavior so `tmp/` and fixture-like content
         are excluded by default.

- [x] Sprint 07 - CI Parity And Regression Coverage
  - Path: `./sprints/07-ci-parity-and-regression-coverage/sprint.md`
  - Goal: make local and CI coverage match for the repository-integrity,
      governance, and workflow checks
  - Depends on: `Sprint 06 - Repository Integrity Validators`
  - Validation focus: task-to-CI parity, subprocess regression coverage,
      fixture quality, and reproducible failure messages
  - Evidence folder: `./sprints/07-ci-parity-and-regression-coverage/evidence/`
  - Subtasks:
        - [x] Add Taskfile entrypoints for the new integrity checkers and ensure
         `check` is the closest local CI mirror.
        - [x] Extend `.github/workflows/quality.yml` so workflow regression tests
         and the new integrity baseline run in CI.
        - [x] Add pass and fail fixtures for inventory drift, version drift,
         broken references, path-case mismatches, and ignored `tmp/` scope.

- [x] Sprint 08 - Workflow Placeholder Hardening
  - Path: `./sprints/08-workflow-placeholder-hardening/sprint.md`
  - Goal: make unresolved scaffold placeholders visible and optionally blocking
      for generated initiative output
  - Depends on: `Sprint 07 - CI Parity And Regression Coverage`
  - Validation focus: placeholder token contract clarity, deterministic output,
      strict-mode behavior, and regression coverage for generated initiative
      artifacts
  - Evidence folder: `./sprints/08-workflow-placeholder-hardening/evidence/`
  - Subtasks:
        - [x] Define the placeholder token contract in ub-workflow references or
         docs so the checker validates an explicit rule.
        - [x] Add `check_scaffold_placeholders.py` and integrate it with
         `scaffold_initiative.py` as appropriate.
        - [x] Extend workflow tests with required-versus-optional placeholder
         cases.

- [x] Sprint 09 - Packaging Policy And Targeted Skill Uplift
  - Path: `./sprints/09-packaging-policy-and-skill-uplift/sprint.md`
  - Goal: document the repository packaging contract and improve the weakest or
      least consistent skill surfaces without broad churn
  - Depends on: `Sprint 08 - Workflow Placeholder Hardening`
  - Validation focus: policy clarity, packaging consistency, targeted skill
      improvements, and minimal-diff discipline
  - Evidence folder: `./sprints/09-packaging-policy-and-skill-uplift/evidence/`
  - Subtasks:
        - [x] Create the canonical packaging-policy document and define required
         versus optional skill assets.
        - [x] Decide whether `agents/openai.yaml` is required, optional, or
         deprecated and make the policy enforceable or consistently optional.
        - [x] Deepen `ub-python` and normalize high-value structural inconsistencies
         such as missing output-contract sections where they improve contributor
         guidance.

- [x] Sprint 10 - Freshness And Portability Review
  - Path: `./sprints/10-freshness-and-portability-review/sprint.md`
  - Goal: add warning-only freshness discipline for volatile skills and clarify
      which quality rules are repository policy versus strong defaults
  - Depends on: `Sprint 09 - Packaging Policy And Targeted Skill Uplift`
  - Validation focus: advisory-only behavior, portability clarity, and absence
      of bureaucratic or blocking side effects
  - Evidence folder: `./sprints/10-freshness-and-portability-review/evidence/`
  - Subtasks:
        - [x] Propose freshness metadata or review-cycle markers for high-volatility
         skill surfaces.
        - [x] Clarify policy-versus-default language in the core quality surfaces
         where portability friction is most likely.
        - [x] Confirm that the advisory layer does not weaken the integrity
         baseline or create noisy blocking checks.

- [x] Final Audit - Repository Hardening Final Audit
  - Path: `./sprints/11-final-audit/sprint.md`
  - Goal: verify full implementation completeness, synchronization, and
      follow-up needs
  - Depends on: `Sprint 10 - Freshness And Portability Review`
  - Validation focus: completeness review, documentation synchronization,
      final quality gates, and follow-up audit or refactor review
  - Evidence folder: `./sprints/11-final-audit/evidence/`
  - Subtasks:
        - [x] Confirm no material roadmap scope was missed
        - [x] Confirm documentation and synchronized artifacts are current where
         applicable
        - [x] Ask whether follow-up audits or refactors are wanted and record the
         answer

## Dependency Chain

1. Sprint 01 corrects the `ub-workflow` lifecycle and gate model so later work
   can depend on a real sprint-preparation phase.
2. Sprint 02 propagates that lifecycle across the workflow contracts, guides,
   and companion-agent surfaces.
3. Sprint 03 turns the corrected lifecycle into helper and template behavior
   that can produce real sprint PRDs.
4. Sprint 04 protects those workflow behaviors with regression and resume
   scenarios.
5. Sprint 05 establishes the authoritative public inventory, metadata baseline,
   and `AGENTS.md` path contract that later validators must enforce.
6. Sprint 06 codifies that truth into deterministic repository-wide checkers.
7. Sprint 07 makes those checkers reproducible across local and CI execution.
8. Sprint 08 extends the same integrity posture into `ub-workflow`'s generated
   output surface.
9. Sprint 09 documents packaging policy and applies targeted quality upgrades
   after the structural baseline is in place.
10. Sprint 10 adds advisory freshness and portability follow-through without
    destabilizing the blocking baseline.
11. Final Audit verifies that every prior sprint actually landed and that no
    required synchronized artifact was skipped.

## Validation Focus Per Sprint

1. Sprint 01: lifecycle consistency, gate clarity, session-reset discipline,
   and explicit human review checkpoints.
2. Sprint 02: contract alignment, guide alignment, and elimination of
   placeholder-shell assumptions from workflow-facing docs.
3. Sprint 03: richer roadmap parsing, sprint-preparation behavior, and template
   semantics for execution-ready sprint PRDs.
4. Sprint 04: regression protection for the discovered failure mode,
   session-reset resume order, and final review pauses.
5. Sprint 05: inventory correctness, file-path correctness, public metadata
   consistency, and install-instruction accuracy.
6. Sprint 06: deterministic checker behavior, UTF-8 handling, exact path or
   case validation, and low-noise authoritative-scope enforcement.
7. Sprint 07: local versus CI parity, regression fixture breadth, and clear
   failure reporting.
8. Sprint 08: placeholder token detection accuracy, strict-mode behavior, and
   generated-output scope discipline.
9. Sprint 09: policy clarity, packaging consistency, and focused skill-surface
   improvements with minimal unrelated churn.
10. Sprint 10: advisory freshness usefulness, portability clarity, and absence
    of new blocking noise.
11. Final Audit: completeness review, synchronized artifacts, final validation
    gates, and follow-up review.

## Roadmap Review Checklist

Review this roadmap against the workflow approval gate before setting
`roadmap_ready: pass`.

1. Sprint breakdown completeness: does the roadmap cover the workflow-correction
   prerequisite plus the original hardening work without silently dropping any
   approved scope?
2. Ordering and dependencies: does each sprint depend on the smallest sensible
   predecessor, and does the sequence preserve a stable workflow and integrity
   baseline before broader quality uplift?
3. Scope boundaries and non-goals: does the roadmap keep phase-1 work focused
   on authoritative surfaces and avoid sliding into arbitrary prose policing or
   manifest generation?
4. Validation and documentation expectations: are the validation focus,
   evidence locations, README or roadmap updates, and final-audit obligations
   explicit enough for another operator to resume without chat history?

## Final Audit Step

The final audit must confirm at minimum:

1. roadmap scope was actually executed
2. no material work was silently skipped
3. synchronized docs, tests, and related artifacts are current where applicable
4. required validation has been run or explicitly deferred
5. the user was asked about follow-up audits or refactors
6. the retained note reflects the final state

## Handoff Expectations

1. Resume from `./roadmap.md` first, then open the active or next sprint's
   `sprint.md`, then the latest `closeout.md` once execution has begun.
2. Keep each sprint `sprint.md` standalone so execution does not depend on chat
   history or reopening the master `prd.md`.
3. Save deterministic evidence under the active sprint's `./evidence/` folder
   before changing sprint state.
4. Update this roadmap and `./README.md` after every meaningful sprint status
   change.

## Initiative Completion Condition

The initiative is complete only when:

1. all roadmap items have closeout records
2. the final audit sprint ends with a passing completion decision
3. required validation scenarios are covered and traceable
4. the canonical docs and synchronized artifacts are current
5. `./retained-note.md` has been written with the final follow-up decision
