# Repository Self-Governance Hardening PRD

> This document is the complete standalone product and execution specification for hardening the Uncle Bob / itech-agents repository so that its inventories, documentation, metadata, packaging conventions, workflow assets, and maintenance expectations stay aligned over time.

Date: 2026-04-15
Project name in repository metadata: `uncle-bob`
Local repository inspected for this revision: `/Users/itechnology/Dev/itech-agents`
Primary repository URL: `https://github.com/robert-hoffmann/uncle-bob`
Status: revised after repository truth check and consolidation of prior analysis notes

---

## 1. Executive summary

This repository is already much stronger than a typical skill collection. It has real architecture, layered responsibilities, executable support in key areas, and a meaningful distinction between core policy and specialized skills.

Its strongest traits are:

- a layered instruction model centered on `AGENTS.md`, `ub-quality`, and sibling specialization
- strong separation of concerns across skills
- progressive disclosure through references instead of one giant instruction blob
- real operational tooling in `ub-governance` and `ub-workflow`
- actual tests for some critical paths rather than purely aspirational quality claims

The repository’s main weakness is not conceptual quality. The main weakness is that the maintenance automation has not caught up with the architecture.

The repository still depends on manual consistency across several public surfaces:

- on-disk skills
- on-disk agent definitions
- root registry guidance
- README tables and install instructions
- plugin metadata
- marketplace metadata
- skill-local references and support assets
- workflow scaffolding assets and tests

Since the earlier analysis, the repository has already moved forward in meaningful ways:

- `ub-initiative-flow` has been renamed to `ub-workflow`
- the README has already been updated to refer to `ub-workflow`
- the Taskfile has already been updated to point workflow tests at `ub-workflow`

That means this initiative should not be framed as migration cleanup anymore. The migration is largely done. The actual need now is a durable repository-wide self-governance layer that prevents the next round of drift.

This PRD therefore focuses on four practical outcomes:

1. derive repository truth from canonical tracked files and on-disk assets
2. validate public descriptive surfaces against that truth
3. keep checks precise and low-noise by validating only authoritative surfaces by default
4. define enough schema and packaging policy to reduce accidental drift without turning governance into ceremony

The recommended first implementation slice is intentionally narrow:

- repository catalog integrity checking
- exact path and case validation
- metadata consistency checking across README and plugin surfaces
- validation of skill reference paths and basic structural contracts
- local and CI parity for those checks

Broader ideas such as freshness and maturity remain useful, but they are secondary to getting a reliable integrity baseline in place.

---

## 2. Problem statement

The repository’s core problem is not weak content. It is weak enforcement of repository truth.

The repository is now large and structured enough that manual synchronization is an operational liability. The likely future failure mode is not one dramatic breakage. It is gradual trust erosion caused by silent drift.

Observed categories of risk include:

1. Inventory drift risk
   - skills and agents are described in multiple places
   - there is no repository-wide validator keeping those surfaces aligned

2. Documentation and metadata drift
   - README, root registry guidance, plugin metadata, and marketplace metadata can silently diverge from actual repository contents

3. Rename and deprecation drift
   - `ub-initiative-flow` has already been migrated to `ub-workflow`
   - future renames can leave stale references behind if not validated automatically

4. Path and case drift
   - `AGENTS.md` is the intended canonical root registry standard
   - exact path and case validation is required because legacy casing and copied references create avoidable portability bugs

5. Validation scope ambiguity
   - the repository contains temporary/test-oriented content under `tmp/`
   - integrity tooling that scans too broadly will generate noise and become untrusted

6. Duplication-driven drift
   - consistency across many skills appears to be maintained partly by copied boilerplate rather than strongly enforced shared contracts
   - repeated mistakes can propagate widely when copied

7. Uneven hardening
   - `ub-governance` already includes focused integrity and regression checks
   - `ub-workflow` already includes scripts, assets, and tests
   - many language/framework skills still rely mostly on prose quality and manual upkeep

8. Under-specified metadata and packaging conventions
   - not all packaging expectations are explicit
   - maintainers and contributors cannot always tell what “complete” packaging means for a skill
   - tooling cannot safely depend on loosely implied metadata conventions

9. Volatile guidance risk
   - framework and tooling guidance for Nuxt, Vue, Tailwind, Python, TypeScript, and Copilot customization can age quickly
   - the repository does not yet have an explicit freshness discipline for that volatility

10. Portability and rigidity risk

- some guidance, especially in core-quality surfaces, may be too rigid for broad reuse across diverse downstream repos
- without clearer contracts, “quality baseline” can slide into “one preferred style for everything”

In short: the repository has outgrown informal maintenance.

---

## 3. Why this matters

If this is left alone, the likely outcomes are:

- a skill gets added on disk but not listed in the registry or README
- a removed or renamed skill remains referenced in canonical docs
- plugin or marketplace metadata continues to sound authoritative while no longer matching reality
- install instructions point to paths or filenames that are wrong
- a skill’s `Load References On Demand` paths drift and no one notices until runtime use
- duplicated boilerplate slowly diverges in meaning across skills
- a checker is eventually added but scans too broadly, flags temporary content, and becomes noisy enough to ignore

This matters because the repository is not just documentation. It is operational instruction infrastructure for downstream agent behavior. If it cannot describe itself accurately, people will stop trusting it — gradually, quietly, and correctly.

Self-governance hardening turns silent drift into early visible failure.

---

## 4. Product vision

Create a repository that is:

1. Authoritative
   - repository truth is derived from canonical tracked files and on-disk assets

2. Self-validating
   - local checks and CI catch inventory drift, stale references, path/case mistakes, metadata mismatches, reference-path breakage, and scaffold issues before they spread

3. Explicitly scoped
   - integrity tooling validates only authoritative repository surfaces by default and ignores temporary or fixture content unless explicitly asked to scan them

4. Contributor-friendly
   - maintainers can add, rename, package, or remove skills and agents without guessing which public surfaces also need updating

5. Evolution-safe
   - fast-moving framework guidance can be reviewed and updated without destabilizing the rest of the repository

6. Portable enough to travel
   - the repository can maintain strong defaults without pretending every downstream repo must share identical stylistic or tooling preferences

---

## 5. Goals

### Primary goals

1. Eliminate drift between on-disk repository inventory and published metadata/documentation surfaces.
2. Add precise repository-wide integrity checks that run both locally and in CI.
3. Define explicit authoritative surfaces and explicit non-authoritative surfaces.
4. Reduce path, case, and reference drift.
5. Validate skill reference paths and basic structural contracts.
6. Improve scaffold completeness visibility for `ub-workflow`.
7. Clarify packaging expectations for skills and agents.

### Secondary goals

1. Introduce advisory freshness discipline for volatile guidance.
2. Add maturity or packaging-tier signaling only if it improves real maintenance and review decisions.
3. Reduce duplication-driven drift where practical.
4. Make the repository safer to reuse across projects with different local conventions.

---

## 6. Non-goals

This initiative is not intended to:

- rewrite the philosophy of the repository
- rewrite every skill for stylistic consistency
- generate all documentation from a master manifest in phase 1
- semantically parse arbitrary markdown prose beyond defined structured sections
- validate temporary, fixture, or generated content as authoritative metadata by default
- preserve transitional documented artifacts forever
- force a maturity-label system in phase 1 if it does not yet drive decisions
- remove strong quality opinions entirely just to appear more generic

---

## 7. Users and stakeholders

### Primary stakeholders

1. Repository maintainer
   - needs dependable low-noise checks and clear failure messages

2. Future contributors
   - need to know what files are authoritative, what references must resolve, and what “complete packaging” means

3. Downstream users of the repo
   - need to trust that README, root registry guidance, metadata, and workflow assets match reality

### Secondary stakeholders

1. Users consuming workflow scaffolds from `ub-workflow`
2. Anyone relying on plugin/marketplace metadata to understand what the repository contains
3. Teams adopting only parts of the repo and needing clarity about what is essential versus optional

---

## 8. Current-state diagnosis

### 8.1 The repository is materially stronger than before

As of this revision:

- `ub-initiative-flow` has been replaced by `ub-workflow`
- `ub-workflow` exists on disk as a real skill
- `ub-workflow` has a corresponding on-disk agent definition
- the README already reflects `ub-workflow`
- the Taskfile already points workflow tests at `ub-workflow`

This means the repository has already corrected one major class of earlier drift.

### 8.2 The repository still lacks a unified integrity layer

The repository still depends on manual maintenance across:

- `.agents/skills/*/SKILL.md`
- `.github/agents/*.agent.md`
- `AGENTS.md` as the intended root registry standard
- `README.md`
- `plugin.json`
- `.github/plugin/marketplace.json`
- skill-local references and support assets

Those surfaces are not yet governed by one repository-level integrity system.

### 8.3 Strong engineering exists, but only in parts of the repo

The earlier analysis was right to highlight that the repository is strongest where it treats skills like products rather than prose.

That is still true now, just with updated naming:

- `ub-governance` is an engineered subsystem with checks, schemas, and regression tests
- `ub-workflow` is an engineered workflow product with templates, scripts, and tests

This is good news, not bad news. It means the repo already contains working patterns for how hardening should look. The gap is that those patterns are not yet elevated to a repository-wide maintenance model.

### 8.4 Transitional artifacts must be handled explicitly

At the time of this revision, `Explore` is still documented as an agent concept, but it is intended to be removed. The repository hardening design must support temporary explicit ignores for this kind of transitional item instead of treating it as either permanent truth or accidental mismatch.

### 8.5 Low-noise validation is a requirement, not a nicety

The repository contains temporary/test-oriented paths such as `tmp/`. Any integrity system that treats every markdown-like surface as authoritative will quickly become noisy and stop being trusted.

### 8.6 Duplication is a structural risk multiplier

The deeper notes were correct that consistency here is partly achieved by duplication rather than reuse.

That does not make the repository weak, but it does create a specific maintenance hazard:

- repeated wording changes can drift in meaning
- repeated path references can drift in casing
- repeated packaging conventions can diverge silently
- the same bug can spread across multiple skills through copy/paste

This initiative should therefore reduce duplication-driven risk through validation and clearer contracts, not just more prose.

---

## 9. Core principles for this initiative

1. Disk truth first
   - use tracked on-disk assets and canonical tracked files as the baseline truth

2. Validate descriptive surfaces against that truth
   - do not rely on descriptive docs as the only inventory source

3. Keep phase 1 practical
   - catch high-value drift first before adding broad policy layers

4. Precision over breadth
   - false positives are a governance failure

5. Explicit exceptions over silent ambiguity
   - if something is temporarily ignored, that should be declared intentionally

6. Exact path and case correctness matter
   - canonical names should be enforced deliberately, not implied loosely

7. Validate actual runtime-facing references
   - if a skill tells the agent to load a reference file, that path should resolve

8. Build on existing hardening
   - reuse and extend the governance and workflow foundations already present in the repository

9. Prefer contracts over duplicated folklore
   - when many skills repeat the same expectations, validate the contract instead of trusting repetition

10. Preserve portability where possible

- the repository can stay opinionated without assuming all downstream repos share one exact style stack or enforcement posture

---

## 10. Proposed solution overview

This initiative should be delivered in two layers.

### Layer 1: Core repository integrity

A. Repository catalog integrity checker
B. Agent and metadata consistency checker
C. Exact path and case validator
D. Skill reference-path and minimal schema validator
E. Local and CI parity for all core checks

### Layer 2: Hardening extensions

F. `ub-workflow` scaffold completeness validator
G. Packaging policy and optional tier signaling
H. Advisory freshness policy for volatile references
I. Selective refactoring of high-duplication shared conventions where validation alone is insufficient

The recommendation is to ship Layer 1 first.

---

## 11. Detailed product requirements

## 11.1 Repository catalog integrity checker

### Requirement

The repository must have a canonical integrity checker that derives baseline inventory from tracked on-disk skills and validates structured public surfaces against that baseline.

### Proposed file

- `.agents/skills/ub-governance/scripts/check_repo_catalog.py`

### Canonical inputs

- `.agents/skills/*/SKILL.md`
- `.github/agents/*.agent.md`
- root `AGENTS.md`
- `README.md`
- `plugin.json`
- `.github/plugin/marketplace.json`

### Default ignore scope

The checker must ignore the following by default unless explicitly configured otherwise:

- `tmp/`
- fixtures
- generated outputs
- examples not declared as canonical surfaces

### Functional behavior

The checker must:

1. discover all skills from `.agents/skills/*/SKILL.md`
2. discover all agent definitions from `.github/agents/*.agent.md`
3. parse the canonical skills and agents listed in the root `AGENTS.md` registry tables
4. parse the structured skill and agent tables in `README.md`
5. validate relevant inventory and count claims in `plugin.json` and `.github/plugin/marketplace.json`
6. report mismatches with file and line detail when possible
7. exit non-zero on real violations
8. support an explicit temporary ignore list for transitional entries such as `Explore`

### Example failures it should catch

- a skill exists on disk but is missing from `AGENTS.md`
- a skill is listed in `README.md` but does not exist on disk
- a renamed skill such as `ub-initiative-flow` is still referenced in a canonical surface
- marketplace metadata claims a count that does not match tracked assets
- an agent is documented but not present on disk and not listed in the explicit transitional ignore set

### Example output

```text
ERROR: Skill present on disk but missing from AGENTS.md: ub-workflow
ERROR: README.md references removed skill name: ub-initiative-flow
ERROR: Marketplace metadata claims 5 agents, but 4 tracked .agent.md files exist
WARNING: Transitional agent entry ignored by policy: Explore
```

---

## 11.2 Minimal skill schema and reference validator

### Requirement

Every skill must comply with a practical structural contract, and every canonical runtime-facing reference path in a skill must resolve.

### Proposed files

- `.agents/skills/ub-governance/references/skill-frontmatter.schema.json`
- `.agents/skills/ub-governance/scripts/check_skill_schema.py`

### Phase-1 contract

Each `SKILL.md` must contain:

- YAML frontmatter
- `name`
- `description`
- frontmatter `name` matching the parent directory name
- readable UTF-8 content

The validator should also confirm that canonical referenced relative paths in the skill actually exist, especially in patterns such as:

- `Read \`references/...\``
- `Read \`docs/...\``
- `Use \`scripts/...\``
- other explicit path-style guidance that the agent is expected to follow at runtime

### Why this matters

The deeper notes correctly identified that repository integrity is not just about top-level inventory. It is also about whether the repository’s own usage instructions resolve to real assets.

### Deferred contract ideas

The following may be added later if they prove useful and low-noise:

- stricter required section taxonomy
- support asset conventions by skill type
- volatility metadata
- maturity metadata

### Rationale

Start with structural correctness and reference validity, not ceremonial prose policing.

---

## 11.3 Agent and package metadata validator

### Requirement

The repository must validate that package and marketplace metadata still describe the real repository contents accurately.

### Proposed file

- `.agents/skills/ub-governance/scripts/check_package_metadata.py`

### Functional behavior

The validator must:

1. compare declared counts and inventory-like claims against tracked skill and agent files
2. validate that referenced repository paths exist and use canonical casing
3. report stale references to removed or renamed skills/agents
4. respect the explicit transitional ignore list for items intentionally pending removal

### Example failures it should catch

- `.github/plugin/marketplace.json` claims five agents when only four tracked agent files exist and the fifth is merely a temporary documented artifact
- package metadata describes workflow assets using a stale renamed skill path

---

## 11.4 Path and case validator

### Requirement

The repository must validate exact path and case correctness for canonical repository surfaces.

### Proposed file

- `.agents/skills/ub-governance/scripts/check_repo_paths.py`

### Canonical rule

The intended root registry standard is `AGENTS.md`, and repository guidance should converge on that exact path and casing.

### Functional behavior

The validator must:

1. build a canonical tracked path index from git
2. extract path-like references from canonical surfaces only
3. validate exact path existence and exact casing against tracked paths
4. report line-level mismatches when possible
5. ignore non-authoritative surfaces by default

### Example failures it should catch

- `AGENTS.MD` referenced where `AGENTS.md` is the intended standard
- `skill.md` referenced where `SKILL.md` is the tracked canonical file
- stale path references under renamed workflow surfaces

### Important constraint

Do not attempt speculative path extraction from arbitrary prose. Validate explicit path-like references and structured sections only.

---

## 11.5 ub-workflow scaffold completeness validation

### Requirement

`ub-workflow` scaffold generation must make unresolved placeholders visible and optionally fail in strict mode.

### Proposed files

- `.agents/skills/ub-workflow/scripts/check_scaffold_placeholders.py`
- update `.agents/skills/ub-workflow/scripts/scaffold_initiative.py`
- tests under `.agents/skills/ub-workflow/tests/`

### Functional behavior

After scaffold generation, the tooling must:

1. scan generated initiative output for unresolved placeholder tokens
2. classify unresolved placeholders as required or optional
3. print a deterministic unresolved placeholder summary
4. optionally fail in strict mode when required placeholders remain

### Important scope rule

Placeholder checks apply to generated initiative artifacts, not to canonical template files by default.

### Why this matters

The deeper notes correctly observed that scaffold generation is safe against clobbering but not strict enough about completeness. That is a real quality gap worth closing.

### Example output

```text
Scaffold created at ./.ub-workflows/initiatives/2026-04-15-example
Unresolved placeholders:
- REPLACE_OWNER (optional)
- REPLACE_VALIDATION_COMMANDS (optional)
```

### Strict-mode failure example

```text
ERROR: Required placeholder still unresolved after scaffold render: REPLACE_INITIATIVE_NAME
```

---

## 11.6 Packaging policy and optional tier signaling

### Requirement

The repository should define what “complete packaging” means for a skill and whether that packaging level is visible.

### Problem being solved

The deeper notes were right that packaging expectations are currently under-specified:

- some skills have agents
- some have scripts/tests/assets/docs
- some are intentionally prose-first
- but the repository does not make the distinction explicit enough for contributors or tooling

### Proposed deliverable

- `docs/skill-schema.md` or equivalent canonical packaging-policy document

### Minimum policy questions to answer

1. Which skill assets are always required?
2. Which are optional?
3. When should a skill include `agents/`?
4. When should a skill include `scripts/` and `tests/`?
5. Which metadata fields are safe for tools to depend on?

### Optional tier model

If useful, the repo may use lightweight packaging tiers such as:

- Base: `SKILL.md` plus required references
- Operational: Base plus scripts/tests/assets/docs as needed

### Constraint

Do not make this phase-1 mandatory unless it directly improves contributor behavior or automation quality.

---

## 11.7 Freshness discipline for volatile references

### Requirement

Fast-moving framework guidance should have an advisory freshness policy.

### Candidate high-volatility areas

- Tailwind
- Nuxt
- Vue
- TypeScript
- Python ecosystem tooling recommendations
- Copilot customization behavior and vendor-specific conventions

### Suggested metadata

This may live either in frontmatter or adjacent review metadata:

```yaml
volatility: high
reviewed_at: 2026-04-15
review_cycle: quarterly
```

### Policy

- freshness should be warning-first, not blocking by default
- stable principles should be distinguishable from volatile setup recipes
- review timestamps should help prioritization, not become performative bureaucracy

### Additional caution

The deeper notes correctly pointed out that “latest stable” is philosophically right but operationally underdefined. The freshness layer should therefore guide review rather than pretend to eliminate judgment.

---

## 11.8 Portability guardrails for core quality surfaces

### Requirement

Core repository guidance should remain strong, but it should be explicit about what is mandatory repository policy versus what is recommended house style.

### Problem being solved

The deeper notes raised a fair concern that `ub-quality` may be too rigid to scale cleanly across diverse downstream repos if every opinion is treated as universally binding.

### Proposed outcome

This initiative should not weaken the repository’s standards, but it should clarify:

- which constraints are fundamental repository policy
- which constraints are style defaults
- which constraints may need explicit downstream opt-out or adaptation

### Why this matters

This improves portability without gutting the repository’s identity.

---

## 12. User stories

### Maintainer stories

1. As a maintainer, when I add or remove a skill, CI should tell me exactly which canonical surfaces are out of sync.
2. As a maintainer, when I rename a workflow skill or agent, stale references should fail quickly.
3. As a maintainer, when I document a transitional item like `Explore`, I want that exception to be explicit rather than silent.
4. As a maintainer, I want integrity tooling to ignore temporary content by default so I can trust its output.
5. As a maintainer, I want runtime-facing skill references validated so I know instructions are actually usable.
6. As a maintainer, I want clearer packaging expectations so contributors do not have to reverse-engineer the repository’s conventions.

### Contributor stories

1. As a contributor, I want a clear definition of authoritative files so I know what must stay aligned.
2. As a contributor, I want local checks and CI to agree.
3. As a contributor using `ub-workflow`, I want unresolved placeholders to be obvious immediately.
4. As a contributor creating a new skill, I want to know what metadata and support assets are expected.

### Consumer stories

1. As a downstream user, I want to trust that the repository’s skill and agent descriptions match the actual repository.
2. As a downstream user, I want setup guidance to point at the right canonical filenames and paths.
3. As a downstream user, I want to understand whether a skill is prose-only guidance or a more operationally hardened subsystem.

---

## 13. Scope

## In scope

- repository-wide inventory checks across on-disk skills, on-disk agents, `AGENTS.md`, `README.md`, `plugin.json`, and `.github/plugin/marketplace.json`
- exact tracked path and case validation for canonical repository surfaces
- explicit temporary ignore handling for transitional entries such as `Explore`
- low-noise structured parsing of tables and explicit path references
- local Taskfile and CI parity for core integrity checks
- `ub-workflow` scaffold placeholder visibility and strict-mode support
- minimal skill schema and reference-path validation
- packaging-policy clarification
- advisory freshness design
- clearer distinction between mandatory policy and more opinionated defaults where needed for portability

## Out of scope

- full generation of docs from a central manifest in phase 1
- semantic parsing of arbitrary README prose
- immediate deep test retrofits for every skill
- forced maturity labeling across all skills before it is useful
- treating `tmp/` or other temporary content as authoritative repository truth by default
- removing strong repository opinions just to maximize generic reuse

---

## 14. Success metrics

### Leading indicators

1. Zero mismatches between on-disk skill inventory and structured registry surfaces.
2. Zero mismatches between on-disk agent inventory and structured metadata surfaces, excluding explicit transitional ignores.
3. Zero canonical path/case mismatches in validated repository surfaces.
4. Zero broken canonical runtime-facing reference paths in validated skills.
5. Zero false positives from temporary or fixture content in default integrity-check mode.
6. Local Taskfile checks and CI run the same integrity suite.
7. `ub-workflow` scaffold checks report unresolved placeholders deterministically.

### Lagging indicators

1. future skill/agent renames are caught automatically when docs lag behind
2. repository metadata remains trustworthy after multiple iterative updates
3. contributors do not need informal tribal knowledge to keep repository surfaces aligned
4. consumers can better distinguish between lightly packaged and operationally hardened skills

---

## 15. Risks and mitigations

### Risk 1: Checker noise kills trust

Mitigation:

- validate only canonical surfaces by default
- keep explicit ignore lists small and reviewable
- prefer precise failures over broad heuristics

### Risk 2: Scope expands too early

Mitigation:

- ship core integrity first
- defer broader policy layers until the baseline is solid

### Risk 3: Freshness metadata becomes theater

Mitigation:

- keep freshness advisory initially
- separate stable principles from volatile recipes

### Risk 4: Transitional exceptions become permanent clutter

Mitigation:

- require explicit ignore entries for temporary exceptions
- review and remove them deliberately

### Risk 5: Canonical filename migration creates temporary inconsistency

Mitigation:

- standardize future guidance on `AGENTS.md`
- let path/case validation make any residual legacy casing visible

### Risk 6: Packaging policy becomes bureaucratic

Mitigation:

- keep packaging policy minimal and decision-oriented
- define only what contributors and tooling actually need

### Risk 7: Portability concerns get ignored because the repo is internally coherent

Mitigation:

- explicitly distinguish non-negotiable repository policy from more opinionated defaults
- preserve strong standards without pretending every downstream repo must use the exact same enforcement posture

---

## 16. Dependencies and assumptions

This PRD assumes:

- the repository will continue using `.agents/skills/` and `.github/agents/` as canonical asset roots
- the intended root registry filename standard is `AGENTS.md`
- `ub-workflow` is the canonical successor to `ub-initiative-flow`
- existing governance scripts under `ub-governance` are the best place to host repository-wide integrity tooling initially
- `Explore` is temporary and intended for removal, not a permanent on-disk agent requirement
- skill-local path references are part of real repository behavior and should be validated as such

---

## 17. Rollout plan

## Phase 0: truth alignment and scope definition

1. declare canonical repository surfaces in writing
2. declare default ignored surfaces in writing
3. declare the temporary ignore treatment for `Explore`
4. converge future documentation and planning on `AGENTS.md`

## Phase 1: repository integrity baseline

1. implement repository catalog checker
2. implement package/marketplace metadata checker
3. implement exact path/case validator
4. wire all three into local developer workflow and CI

## Phase 2: structural hardening

1. implement minimal skill schema validation
2. validate canonical skill reference paths
3. add targeted test coverage for new checks

## Phase 3: workflow hardening

1. add `ub-workflow` generated-output placeholder validator
2. add strict-mode support where useful
3. ensure deterministic test coverage for scaffold validation

## Phase 4: policy clarification

1. define minimal packaging policy for skills and agents
2. clarify portability boundaries for core-quality guidance
3. add freshness review metadata only if maintainers still want it
4. add optional tier signaling only if it solves a real problem

---

## 18. Maintainer action list with examples

## Action 1: create the repository catalog checker

Deliverables:

- enumerate skills from `.agents/skills/*/SKILL.md`
- enumerate agents from `.github/agents/*.agent.md`
- parse structured skill and agent tables from `AGENTS.md` and `README.md`
- compare those surfaces deterministically

## Action 2: add metadata consistency checking

Deliverables:

- validate skill and agent count claims in plugin and marketplace metadata
- validate that those claims respect temporary ignore policy where applicable

## Action 3: validate exact path casing

Deliverables:

- build canonical tracked path index from git
- validate explicit path references in canonical surfaces
- report exact mismatches with file and line detail

## Action 4: validate skill runtime-facing references

Deliverables:

- verify `Load References On Demand` paths exist
- verify explicit script/doc/reference paths in skills exist where they are presented as canonical usage guidance

## Action 5: improve ub-workflow scaffold completeness visibility

Deliverables:

- scan generated initiative output for unresolved placeholders
- classify placeholders by severity
- support optional strict failure mode

## Action 6: align local workflow and CI

Deliverables:

- Taskfile tasks covering new integrity scripts
- CI tasks matching the same integrity coverage
- no separate hidden CI-only checks for the baseline suite

## Action 7: add minimal packaging-policy documentation

Deliverables:

- define required versus optional skill assets
- define expectations for agents/scripts/tests/docs where relevant
- keep the policy small and actionable

## Action 8: consider advisory policy layers only after baseline integrity ships

Deliverables:

- freshness guidance if still needed
- optional tier signaling if it serves maintainers rather than aesthetics
- clarified distinction between mandatory policy and more opinionated defaults if portability friction persists

---

## 19. Example deliverables

Expected concrete outputs from this initiative may include:

- `.agents/skills/ub-governance/scripts/check_repo_catalog.py`
- `.agents/skills/ub-governance/scripts/check_package_metadata.py`
- `.agents/skills/ub-governance/scripts/check_repo_paths.py`
- `.agents/skills/ub-governance/scripts/check_skill_schema.py`
- `.agents/skills/ub-governance/references/skill-frontmatter.schema.json`
- `.agents/skills/ub-workflow/scripts/check_scaffold_placeholders.py`
- `docs/skill-schema.md` or equivalent packaging-policy doc
- Taskfile tasks for all core checks
- CI workflow updates invoking the same checks
- documented temporary-ignore mechanism for transitional entries such as `Explore`

---

## 20. Acceptance criteria

This initiative is complete when all of the following are true:

1. The repository has a working catalog integrity checker.
2. The repository has a working metadata consistency checker.
3. The repository has a working exact path/case validator.
4. The repository has a working minimal skill schema/reference validator.
5. Core integrity checks run locally and in CI with the same baseline coverage.
6. `ub-workflow` scaffold placeholder validation exists and reports deterministically.
7. The baseline integrity suite ignores temporary/test surfaces by default.
8. The repository can tolerate explicit temporary exceptions such as `Explore` without hiding real mismatches.
9. Canonical future guidance converges on `AGENTS.md`.
10. Contributors have a documented minimal packaging contract to follow.

---

## 21. Open questions

1. Should the temporary ignore list live in code, config, or repository metadata?
2. Should marketplace metadata validate only counts, or also constrained descriptive phrases?
3. Should path/case validation be strict for all canonical surfaces immediately, or staged?
4. When the repository fully converges on `AGENTS.md`, should any residual legacy-cased file be automatically treated as a violation?
5. Is freshness metadata worth introducing before the baseline integrity suite has proven stable?
6. Would a generated catalog become worthwhile later, or is disk truth sufficient long-term?
7. How much of the repository’s stylistic rigidity should be treated as invariant policy versus reusable default?
8. Should packaging expectations stay purely documentary, or should they become partially enforceable by tooling?

---

## 22. Recommended execution order

1. Build the repository catalog checker.
2. Build the package/marketplace metadata checker.
3. Build the exact path/case validator.
4. Add Taskfile and CI parity for those checks.
5. Add minimal skill schema and runtime-reference validation.
6. Add `ub-workflow` placeholder completeness validation.
7. Document minimal packaging policy.
8. Consider advisory freshness policy.
9. Consider optional tier signaling last.

---

## 23. Final recommendation

Do not overengineer this.

The repository does not need a grand content-management system. It needs a reliable self-checking baseline grounded in tracked files and canonical repository surfaces.

The best next move is to ship the smallest integrity system that catches real drift:

- inventory mismatches
- stale renamed references
- path/case mistakes
- metadata count drift
- broken skill reference paths
- low-noise workflow scaffold validation

Then, and only then, add the lighter policy layers around packaging clarity, freshness, and portability guardrails.

That solves the real problem without turning governance into ceremony.

---

## 24. Durable note for future revisit

This PRD intentionally assumes no memory of previous discussion.

The key durable truths it captures are:

- `ub-workflow` is the canonical successor to `ub-initiative-flow`
- the README and Taskfile have already been updated for that rename
- `AGENTS.md` is the intended canonical root registry standard
- `Explore` is a temporary documented artifact intended for removal
- the repository’s highest-value missing capability is a low-noise, repository-wide integrity layer
- stronger repository-wide validation should absorb the best lessons from the older analysis notes without requiring those notes to remain as separate source documents

---

## 25. Verification addendum (2026-04-16)

This addendum records the post-PRD verification work that was completed before
roadmap generation so the initiative can proceed without relying on chat
history.

### Verified external contract notes

1. Official VS Code and GitHub Copilot documentation now confirm that
   `AGENTS.md` is the supported agent-instructions filename for the relevant
   environments that this repository targets.
2. Official VS Code custom-agent documentation distinguishes built-in agents
   from workspace-defined custom agents discovered from `.github/agents/`.
3. That distinction means `Explore` should be removed from repository inventory
   and metadata counts, while remaining valid as a built-in subagent reference
   inside local `.agent.md` files when the platform supports it.
4. For filename, instructions, and custom-agent behavior, official GitHub and
   VS Code documentation are the primary sources of truth for this initiative.
   Research papers may still inform later quality or portability work, but they
   are secondary for product-contract questions.

### Verified repository truth notes

1. `ub-workflow` has fully replaced `ub-initiative-flow` on disk; the old name
   no longer appears in canonical repository surfaces outside planning notes.
2. `Taskfile.yml` already includes `test-workflow`, but `.github/workflows/quality.yml`
   does not yet run the workflow regression suite in CI.
3. `pyproject.toml` version metadata currently diverges from `plugin.json` and
   `.github/plugin/marketplace.json`.
4. The repository currently uses `AGENTS.MD` on disk, so the roadmap treats the
   `AGENTS.MD` to `AGENTS.md` change as an explicit migration step rather than
   as an already-completed fact.

### Derived planning decisions

1. Sprint 01 should align public inventory, remove `Explore` from published
   repository agent counts, and complete the root-registry rename to
   `AGENTS.md`.
2. The repository-wide integrity baseline should validate only authoritative
   surfaces by default and exclude `tmp/` plus fixture-like content unless
   explicitly asked to scan broader scope.
3. The initiative should use a Level 1 governance bridge with the `lean`
   profile so validation, final audit language, and follow-up decisions are
   explicit without forcing ADR or evidence-heavy workflows in every sprint.
