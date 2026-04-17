# Sprint PRD

## Summary

Document the repository's packaging contract and apply only the highest-value
skill-surface improvements that the new integrity baseline makes necessary.
This sprint should make it clear what assets are required versus optional for a
skill or agent package, settle the stance on `agents/openai.yaml`, and deepen
the weakest or least consistent skill surfaces without turning the initiative
into a repo-wide rewrite.

## Scope

1. Create the canonical packaging-policy document that defines required versus
 optional skill assets and makes the packaging contract actionable for
 contributors.
2. Decide whether `agents/openai.yaml` is required, optional, or deprecated and
 make that decision explicit rather than leaving it implied.
3. Deepen `./.agents/skills/ub-python/` so its references and guidance better
 match the repository's actual Python usage and quality expectations.
4. Normalize only the highest-value structural inconsistencies, such as missing
 output-contract sections, when they materially improve contributor guidance.

## Dependencies

1. Sprint 08 must complete first so the workflow surface is stable before
 broader packaging policy and skill-surface documentation changes begin.
2. Use `./prd.md` sections 11.6, 13, 17 phase 4, 18 action 7, and 20 as the
 product contract for packaging-policy scope and restraint.
3. Use the outputs of the new integrity baseline to decide what must become
 policy instead of inventing requirements that the repository does not really
 need.

## Repository Truth At Sprint Start

1. The repository currently has a mix of prose-first and operationally hardened
 skills, but no canonical document that defines what packaging completeness
 means.
2. `./.agents/skills/ub-python/` is a likely candidate for targeted reference
 and structural improvement once the baseline integrity layer is in place.
3. The status of `agents/openai.yaml` is still under-specified and therefore
 hard for contributors or tooling to interpret consistently.
4. This sprint should stay deliberately narrow: it is not a full normalization
 pass across every skill.

## Chosen Path

Write one minimal policy document that answers the real packaging questions,
then apply targeted improvements only where the new policy or integrity checks
make a gap obvious. This keeps the sprint decision-oriented and avoids turning
policy clarification into broad stylistic cleanup.

## Rejected Alternative

Attempt a repo-wide skill-surface normalization pass at the same time as the
packaging policy.

Pros:

1. Could increase superficial consistency quickly.
2. Might surface hidden drift in one large pass.

Cons:

1. Expands scope far beyond the PRD's recommended first implementation slice.
2. Makes it harder to tell which changes are policy-driven versus cosmetic.
3. Risks delaying real policy clarity behind large prose edits.

## Affected Areas

1. `./docs/skill-schema.md` or the chosen packaging-policy document path
2. `./.agents/skills/ub-python/`
3. Any small number of other skill files whose structural inconsistencies are
 explicitly selected for correction in this sprint
4. Potentially `./README.md` or `./AGENTS.md` only if the packaging policy must
 be surfaced publicly after it is written

## Validation Plan

1. Run `npx --yes markdownlint-cli2` against the new packaging-policy document
 and any touched skill documentation.
2. Re-run the relevant integrity checks introduced in Sprint 02 if packaging or
 skill-structure changes affect their expected outputs.
3. Record the chosen `agents/openai.yaml` policy decision and the reasons for
 it in `./evidence/` so Sprint 10 and Sprint 11 can treat it as a
 settled contract.
4. If `ub-python` changes touch Python support files or examples, run the most
 relevant lint or structural checks and record the exact command outcomes in
 the sprint closeout.
5. For the Level 1 `lean` governance bridge, record why the chosen policy is
 minimal enough to avoid bureaucracy while still being explicit.

## Exit Criteria

1. A canonical packaging-policy document exists and answers the minimum policy
 questions named in the PRD.
2. The `agents/openai.yaml` stance is explicit and no longer implied.
3. The selected high-value skill-surface improvements are complete, validated,
 and recorded for Sprint 06 and the final audit.

## Final Audit Checklist

Use this checklist only when this sprint is the final audit sprint.

- [ ] roadmap scope was actually executed or explicitly deferred
- [ ] no material work was silently skipped
- [ ] initiative-level validation is recorded and traceable
- [ ] relevant documentation and synchronized artifacts reflect the shipped behavior
- [ ] follow-up audit or refactor decisions were captured
- [ ] `retained-note.md` is ready to record the final state

## Handoff Expectation

Sprint 10 should read this sprint's `closeout.md` first, then the final
packaging-policy document. Its first task is to add warning-only freshness
discipline for volatile skill guidance and clarify which core quality rules are
repository policy versus strong defaults for downstream portability.

## Definition Of Done

This sprint is done only when all of the following are true:

1. planned functionality is complete or explicitly blocked
2. known in-scope issues are documented
3. required validation is run or explicitly deferred
4. relevant documentation and synchronized artifacts are updated or explicitly marked unchanged
5. validation evidence is recorded and traceable
6. governance bridge requirements are satisfied or explicitly marked not applicable
7. closeout is current and resumable
