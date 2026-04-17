# Sprint PRD

## Summary

Build the repository-wide integrity baseline under `ub-governance` after Sprint
01 aligns the public inventory and metadata surfaces. This sprint should add
deterministic, low-noise validators for repository catalog integrity, package
metadata consistency, exact path and case correctness, and minimal skill
schema/runtime-reference validity, while preserving the existing direct-CLI
script pattern already used in `ub-governance`.

## Scope

1. Implement `check_repo_catalog.py` for disk-versus-registry comparison across
 skills, custom agents, the root registry, README inventory tables, and
 package metadata surfaces.
2. Implement `check_package_metadata.py` for version and inventory-like claim
 validation across `./plugin.json` and
 `./.github/plugin/marketplace.json`.
3. Implement `check_repo_paths.py` for exact tracked path and case validation
 across canonical repository surfaces.
4. Implement `check_skill_schema.py` plus any minimal schema asset needed to
 validate skill frontmatter shape and runtime-facing reference paths.
5. Define the low-noise ignore-scope behavior so `./tmp/`, fixtures, and other
 non-authoritative content stay excluded by default.

## Dependencies

1. Sprint 05 must finish first so the public inventory, canonical filename, and
 version metadata are aligned before the new validators are authored.
2. Use `./prd.md` sections 11.1 through 11.4, section 17 phase 1, section 18
 actions 1 through 4, and section 25 derived planning decisions as the
 product contract for the baseline checker suite.
3. Reuse the existing direct-CLI validation pattern already present in
 `./.agents/skills/ub-governance/scripts/check_skill_integrity.py` and the
 subprocess-style regression approach already used in the governance test
 suite.

## Repository Truth At Sprint Start

1. `./.agents/skills/ub-governance/scripts/` already contains focused CLI
 validators such as `check_skill_integrity.py`, `check_claim_register.py`,
 and `check_test_signal.py`.
2. `./.agents/skills/ub-governance/tests/governance_scripts/` already provides
 the current subprocess-style regression-test pattern for governance scripts.
3. `./.agents/skills/` currently contains ten tracked skills and
 `./.github/agents/` currently contains four tracked custom agent
 definitions.
4. `./tmp/` and other fixture-like content must remain outside the default
 authoritative scan scope or the new checkers will become noisy and lose
 trust.
5. No repository-wide checker suite currently validates all of the canonical
 public inventory, metadata, path, and skill-reference surfaces together.

## Chosen Path

Implement four focused CLI scripts under `./.agents/skills/ub-governance/scripts/`
using the existing house pattern, and introduce only the smallest shared helper
surface that remains safe for direct script execution under `uv run python`.
This keeps the baseline explicit, debuggable, and composable while still
reducing duplicated repo-walking and UTF-8 parsing logic when duplication would
otherwise be substantial.

## Rejected Alternative

Create one monolithic repository checker that handles catalog, metadata, paths,
and skill schema in a single large script.

Pros:

1. One entrypoint is easy to discover.
2. Shared logic is trivial because everything lives in one file.

Cons:

1. Failures become harder to localize and reason about.
2. Future CI and Taskfile parity work becomes coarser than necessary.
3. The script would be harder to test and more likely to grow into an
 over-coupled governance subsystem.

## Affected Areas

1. `./.agents/skills/ub-governance/scripts/`
2. `./.agents/skills/ub-governance/tests/governance_scripts/`
3. `./.agents/skills/ub-governance/references/skill-frontmatter.schema.json`
 if a dedicated schema artifact is introduced
4. `./AGENTS.md`, `./README.md`, `./plugin.json`,
 `./.github/plugin/marketplace.json`, and `./.agents/skills/*/SKILL.md` as
 validated inputs rather than as primary implementation surfaces

## Validation Plan

1. Run each new script directly with `uv run python` to confirm it is
 executable as a standalone CLI without relying on package installation.
2. Run `uv run python -m unittest discover -s
 .agents/skills/ub-governance/tests/governance_scripts -p 'test_*.py' -v`
 after adding regression coverage for pass and fail cases.
3. Use fixture inputs or temporary repositories to prove that `./tmp/` and
 other non-authoritative surfaces are ignored by default.
4. Record example pass/fail outputs for the four new scripts in `./evidence/`
 so Sprint 07 can wire the exact commands into local and CI parity work.
5. For the Level 1 `lean` governance bridge, document the final authoritative
 surface list and ignore-scope decision in the sprint closeout.

## Exit Criteria

1. The repository has focused baseline checkers for catalog integrity, package
 metadata, path/case correctness, and skill schema/runtime-reference
 validity.
2. Each checker has direct CLI execution proof and regression-test coverage for
 at least one pass and one fail case.
3. Sprint closeout names the stable script interfaces and commands Sprint 07
 should wire into Taskfile and CI parity.

## Final Audit Checklist

Use this checklist only when this sprint is the final audit sprint.

- [ ] roadmap scope was actually executed or explicitly deferred
- [ ] no material work was silently skipped
- [ ] initiative-level validation is recorded and traceable
- [ ] relevant documentation and synchronized artifacts reflect the shipped behavior
- [ ] follow-up audit or refactor decisions were captured
- [ ] `retained-note.md` is ready to record the final state

## Handoff Expectation

Sprint 07 should read this sprint's `closeout.md` first, then inspect the final
CLI entrypoints and test locations under `./.agents/skills/ub-governance/`.
Its first task is to wire the new checker commands into `./Taskfile.yml`,
extend `./.github/workflows/quality.yml`, and add any missing regression
fixtures so local `task check` is the closest parity mirror of CI.

## Definition Of Done

This sprint is done only when all of the following are true:

1. planned functionality is complete or explicitly blocked
2. known in-scope issues are documented
3. required validation is run or explicitly deferred
4. relevant documentation and synchronized artifacts are updated or explicitly marked unchanged
5. validation evidence is recorded and traceable
6. governance bridge requirements are satisfied or explicitly marked not applicable
7. closeout is current and resumable
