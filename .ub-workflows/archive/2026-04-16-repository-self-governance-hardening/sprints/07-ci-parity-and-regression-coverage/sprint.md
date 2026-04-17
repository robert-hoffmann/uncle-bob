# Sprint PRD

## Summary

Make local and CI quality coverage match for the repository-integrity,
governance, and workflow checks that exist after Sprint 02. This sprint should
extend the existing Taskfile and GitHub Actions quality workflow so the new
integrity baseline, the existing governance regression suite, and the existing
workflow regression suite all run through one visible, reproducible path.

## Scope

1. Add Taskfile entrypoints for the new repository-integrity checkers and make
 `task check` the closest local parity mirror of CI.
2. Extend `./.github/workflows/quality.yml` so the workflow regression suite
 runs in CI alongside markdown, YAML, Ruff, and governance checks.
3. Add pass and fail fixtures that cover inventory drift, version drift,
 stale references, path-case mismatches, broken skill references, and ignored
 `./tmp/` scope behavior.
4. Keep the CI additions incremental by reusing the existing workflow matrix
 and current direct-CLI test commands rather than inventing a separate CI
 path.

## Dependencies

1. Sprint 06 must complete first so the new checker entrypoints and baseline
 test expectations are stable enough to wire into local and CI parity.
2. Use `./prd.md` sections 14, 17, 18 action 6, and 20 as the product
 contract for local/CI parity and deterministic regression coverage.
3. Build on the current Taskfile and GitHub Actions quality workflow instead of
 replacing them wholesale.

## Repository Truth At Sprint Start

1. `./Taskfile.yml` already defines `test-integrity`, `test-governance`,
 `test-workflow`, and `check`, but `test-integrity` currently points only to
 `check_skill_integrity.py`.
2. `./.github/workflows/quality.yml` currently runs markdown, Ruff, YAML,
 governance integrity, and governance regression checks, but it does not yet
 run `test-workflow`.
3. `./.agents/skills/ub-workflow/tests/` already contains the workflow helper
 regression suite that should be part of CI parity.
4. The repository already uses `uv`, `task`, and GitHub Actions matrices, so
 this sprint should extend the current pattern rather than create a parallel
 one.

## Chosen Path

Extend the existing Taskfile and GitHub Actions matrix in place, then add the
missing fixtures and regression cases around the new integrity scripts. This
keeps parity visible to contributors, preserves the current operator workflow,
and avoids a split where CI does things local developers never run.

## Rejected Alternative

Document the new checker commands but leave CI and local parity unchanged until
later.

Pros:

1. Minimizes immediate workflow-file churn.
2. Defers fixture-building effort.

Cons:

1. Leaves a known trust gap between local and CI behavior.
2. Makes regression coverage optional at the exact moment the baseline checker
 surface is expanding.
3. Violates the PRD's explicit parity goal and delays detection of noisy or
 unstable checks.

## Affected Areas

1. `./Taskfile.yml`
2. `./.github/workflows/quality.yml`
3. `./.agents/skills/ub-governance/tests/governance_scripts/`
4. `./.agents/skills/ub-workflow/tests/`
5. Any new governance or workflow fixture directories needed to exercise pass
 and fail cases deterministically

## Validation Plan

1. Run `task check` locally and confirm it now covers the same integrity,
 governance, workflow, and lint surfaces that CI runs.
2. Run `task test-workflow` directly to confirm the workflow regression suite
 is green before and after CI wiring changes.
3. Re-run the governance and workflow unit-test discovery commands directly if
 fixture failures need isolation.
4. Save fixture descriptions, expected pass/fail cases, and the final task or
 matrix target list in `./evidence/` for later audit.
5. For the Level 1 `lean` governance bridge, record the final parity mapping
 between Taskfile targets and CI jobs in the sprint closeout.

## Exit Criteria

1. Local `task check` is the closest parity mirror of CI for the integrity,
 governance, workflow, and lint baseline.
2. CI runs the workflow regression suite and the new repository-integrity
 checks introduced in Sprint 02.
3. Regression fixtures exist for the high-value drift cases named in the PRD,
 and Sprint closeout records where they live and how they are invoked.

## Final Audit Checklist

Use this checklist only when this sprint is the final audit sprint.

- [ ] roadmap scope was actually executed or explicitly deferred
- [ ] no material work was silently skipped
- [ ] initiative-level validation is recorded and traceable
- [ ] relevant documentation and synchronized artifacts reflect the shipped behavior
- [ ] follow-up audit or refactor decisions were captured
- [ ] `retained-note.md` is ready to record the final state

## Handoff Expectation

Sprint 08 should read this sprint's `closeout.md` first, then inspect the final
Taskfile and CI parity wiring. Its first task is to define the placeholder
token contract for generated initiative artifacts and add deterministic
placeholder-completeness reporting to `ub-workflow` without broadening the
scope to canonical templates.

## Definition Of Done

This sprint is done only when all of the following are true:

1. planned functionality is complete or explicitly blocked
2. known in-scope issues are documented
3. required validation is run or explicitly deferred
4. relevant documentation and synchronized artifacts are updated or explicitly marked unchanged
5. validation evidence is recorded and traceable
6. governance bridge requirements are satisfied or explicitly marked not applicable
7. closeout is current and resumable
