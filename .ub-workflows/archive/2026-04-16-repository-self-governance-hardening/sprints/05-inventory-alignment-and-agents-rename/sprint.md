# Sprint PRD

## Summary

Align the repository's public inventory and metadata surfaces with verified
disk truth before any repository-wide checker work begins. This sprint removes
published `Explore` agent inventory claims while preserving valid built-in
subagent references, converges the root registry path from `AGENTS.MD` to
`AGENTS.md`, and reconciles version drift across the packaging surfaces so
later validators have one trustworthy baseline to enforce.

## Scope

1. Remove `Explore` from published repository agent inventory and count claims
 while preserving legitimate built-in subagent references inside local
 `.agent.md` files.
2. Rename the root registry file from `AGENTS.MD` to `AGENTS.md` and update all
 canonical references, quick-start instructions, and repository-layout text.
3. Reconcile version drift across `./pyproject.toml`, `./plugin.json`, and
 `./.github/plugin/marketplace.json`.
4. Record any explicit temporary exception needed so Sprint 02 can treat the
 aligned public surfaces as authoritative.

## Dependencies

1. Sprint 04 must complete first so the workflow redesign, helper behavior, and
 sprint-preparation regression coverage are already stable before the original
 hardening work begins.
2. Use `./prd.md` section 25 as the verified contract source for `AGENTS.md`,
 built-in-versus-workspace agent behavior, and the current metadata-drift
 facts.
3. Use tracked disk truth from `./.agents/skills/`, `./.github/agents/`,
 `./README.md`, `./plugin.json`, `./.github/plugin/marketplace.json`,
 `./pyproject.toml`, and `./AGENTS.MD`.

## Repository Truth At Sprint Start

1. The root registry file on disk is currently `./AGENTS.MD`, while the PRD
 and verification addendum treat `AGENTS.md` as the intended canonical
 standard.
2. `./README.md` currently lists `Explore` in the public agent inventory even
 though only four tracked `.agent.md` files exist under `./.github/agents/`.
3. `./plugin.json` and `./.github/plugin/marketplace.json` currently report
 version `1.0.0`, while `./pyproject.toml` reports `0.1.0`.
4. `./README.md` quick-start and repository-layout instructions currently refer
 to `AGENTS.MD`.
5. Sprint 06 assumes these public surfaces are aligned before new repository
 integrity validators are introduced.

## Chosen Path

Align the human-facing surfaces first, then build validators against the
corrected baseline. That keeps Sprint 02 focused on durable enforcement instead
of mixing product-surface fixes with validation logic and avoids encoding known
wrong inventory or filename claims into new checker expectations.

## Rejected Alternative

Build the validators first and let them fail against the current repository.

Pros:

1. Forces drift to become visible immediately.
2. Produces early failing examples for future regression tests.

Cons:

1. Conflates known truth-alignment work with validator implementation.
2. Makes it harder to tell whether a failure is a real checker defect or an
 intentionally unfixed public-surface mismatch.
3. Risks baking stale inventory and filename assumptions into Sprint 06.

## Affected Areas

1. `./AGENTS.MD` or its renamed successor `./AGENTS.md`
2. `./README.md`
3. `./plugin.json`
4. `./.github/plugin/marketplace.json`
5. `./pyproject.toml`
6. `./.github/agents/*.agent.md` only when built-in subagent wording must stay
 explicit after `Explore` is removed from published inventory surfaces

## Validation Plan

1. Use targeted repository scans such as
 `rg -n "Explore|AGENTS\\.MD|AGENTS\\.md|\"version\"" README.md AGENTS.MD AGENTS.md plugin.json .github/plugin/marketplace.json pyproject.toml .github/agents` to confirm the before and after state.
2. Run `npx --yes markdownlint-cli2 README.md AGENTS.md` after the registry
 rename and public-doc updates.
3. Re-open `./plugin.json`, `./.github/plugin/marketplace.json`, and
 `./pyproject.toml` to verify the chosen version string is identical in all
 three surfaces.
4. Record before/after inventory counts and the resolved root-registry filename
 in `./evidence/` so Sprint 02 can treat the aligned surfaces as the new
 baseline.
5. For the Level 1 `lean` governance bridge, record any deliberate temporary
 exception or deferral in the sprint closeout instead of leaving it implicit.

## Exit Criteria

1. Public inventory and quick-start surfaces match current disk truth,
 including removal of published `Explore` inventory claims and convergence on
 `AGENTS.md`.
2. Version metadata is reconciled across the three packaging surfaces or any
 deliberate exception is explicitly recorded.
3. Sprint closeout names the aligned surfaces that Sprint 06 should now treat
 as authoritative.

## Final Audit Checklist

Use this checklist only when this sprint is the final audit sprint.

- [ ] roadmap scope was actually executed or explicitly deferred
- [ ] no material work was silently skipped
- [ ] initiative-level validation is recorded and traceable
- [ ] relevant documentation and synchronized artifacts reflect the shipped behavior
- [ ] follow-up audit or refactor decisions were captured
- [ ] `retained-note.md` is ready to record the final state

## Handoff Expectation

Sprint 06 should read this sprint's `closeout.md` first, then re-read
`./AGENTS.md`, `./README.md`, `./plugin.json`,
`./.github/plugin/marketplace.json`, and `./pyproject.toml` before creating
the repository integrity scripts. Its first task is to encode the aligned disk
and metadata truth into deterministic low-noise validators under
`./.agents/skills/ub-governance/scripts/`.

## Definition Of Done

This sprint is done only when all of the following are true:

1. planned functionality is complete or explicitly blocked
2. known in-scope issues are documented
3. required validation is run or explicitly deferred
4. relevant documentation and synchronized artifacts are updated or explicitly marked unchanged
5. validation evidence is recorded and traceable
6. governance bridge requirements are satisfied or explicitly marked not applicable
7. closeout is current and resumable
