# Sprint PRD

## Summary

Add advisory freshness discipline for volatile guidance and clarify the
portability boundaries of the repository's strongest quality surfaces. This
sprint should help maintainers prioritize review of fast-moving framework
guidance without turning freshness into blocking theater, and it should make
clear which core-quality rules are repository policy versus strong house
defaults that downstream users may need to adapt deliberately.

## Scope

1. Propose freshness metadata or review-cycle markers for high-volatility
 skills such as Tailwind, Nuxt, Vue, TypeScript, Python tooling, and Copilot
 customization guidance.
2. Keep the freshness layer warning-only by default and document why it is not
 a blocking phase-1 control.
3. Clarify policy-versus-default language in the core quality surfaces where
 portability friction is most likely.
4. Confirm that the advisory layer does not weaken the baseline integrity suite
 or introduce new bureaucratic checks.

## Dependencies

1. Sprint 09 must complete first so packaging-policy decisions and targeted
 skill uplift are already settled.
2. Use `./prd.md` sections 11.7, 11.8, 15 risks 3 and 7, 17 phase 4, and 18
 action 8 as the product contract for this work.
3. Reuse the baseline integrity and packaging-policy outputs from prior sprints
 rather than inventing a parallel metadata system.

## Repository Truth At Sprint Start

1. The repository contains several high-volatility guidance areas, especially
 around Tailwind, Nuxt, Vue, TypeScript, Python tooling, and Copilot
 customization behavior.
2. The PRD explicitly warns that freshness should be advisory first and that
 stable principles must be distinguished from volatile setup recipes.
3. The repository's core quality surfaces are strong, but the PRD notes that
 portability concerns need clearer wording so downstream users can separate
 hard policy from strong defaults.
4. No freshness-review metadata or portability-boundary clarification currently
 exists as a durable, explicit contract.

## Chosen Path

Add a lightweight warning-only freshness design and make portability boundaries
explicit in the most relevant quality surfaces. This preserves the repository's
strong opinions while preventing the phase-1 hardening effort from expanding
into an overbearing review bureaucracy.

## Rejected Alternative

Make freshness a blocking requirement across volatile skills immediately.

Pros:

1. Forces review discipline quickly.
2. Makes stale high-volatility guidance more visible.

Cons:

1. Conflicts with the PRD's warning-first recommendation.
2. Risks producing noisy blockers before the baseline integrity layer proves
 stable and trusted.
3. Turns advisory review into ceremony instead of maintainable prioritization.

## Affected Areas

1. Volatile skill surfaces under `./.agents/skills/` such as `ub-tailwind/`,
 `ub-nuxt/`, `ub-vuejs/`, `ub-ts/`, `ub-python/`, and
 `ub-customizations/`
2. `./.agents/skills/ub-quality/` or adjacent core-quality references where
 portability-boundary wording needs clarification
3. Any packaging-policy or reference doc updated to host freshness-review
 guidance or policy/default distinctions

## Validation Plan

1. Run `npx --yes markdownlint-cli2` on every touched documentation or skill
 surface.
2. Re-run the baseline integrity suite after changes to confirm the advisory
 layer did not create new blocking failures or invalidate the packaging
 contract.
3. Record the final freshness policy, review-cycle recommendation, and any
 clarified policy-versus-default wording in `./evidence/`.
4. Confirm in the sprint closeout that the freshness layer remains advisory and
 that no CI blocker was introduced by this sprint.
5. For the Level 1 `lean` governance bridge, explicitly note why the chosen
 approach avoids turning the repository into process theater.

## Exit Criteria

1. A warning-only freshness discipline exists for the chosen high-volatility
 surfaces.
2. Policy-versus-default wording is clearer in the core quality surfaces where
 portability concerns matter most.
3. Sprint closeout confirms that the advisory layer did not weaken the baseline
 integrity posture or create new blocking noise.

## Final Audit Checklist

Use this checklist only when this sprint is the final audit sprint.

- [ ] roadmap scope was actually executed or explicitly deferred
- [ ] no material work was silently skipped
- [ ] initiative-level validation is recorded and traceable
- [ ] relevant documentation and synchronized artifacts reflect the shipped behavior
- [ ] follow-up audit or refactor decisions were captured
- [ ] `retained-note.md` is ready to record the final state

## Handoff Expectation

Sprint 11 should read this sprint's `closeout.md` first, then the
updated policy and freshness artifacts. Its first task is to verify that every
prior sprint actually landed, that synchronized docs and validation outputs are
current, and that the user is asked explicitly about follow-up audits or
refactors before any archive step is considered.

## Definition Of Done

This sprint is done only when all of the following are true:

1. planned functionality is complete or explicitly blocked
2. known in-scope issues are documented
3. required validation is run or explicitly deferred
4. relevant documentation and synchronized artifacts are updated or explicitly marked unchanged
5. validation evidence is recorded and traceable
6. governance bridge requirements are satisfied or explicitly marked not applicable
7. closeout is current and resumable
