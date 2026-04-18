# Cross-Skill Authoring Conventions

Use this reference when shaping shared skill authoring patterns across the
catalog.

These conventions are selective, not universal. Apply them where they improve
routing, readability, or operator predictability. Do not force them into skills
where they become boilerplate.

## Shared Conventions Worth Reusing

### 1. Explicit "When Not To Use" Guidance

Add or strengthen a `When Not To Use` section when:

- routing mistakes are realistically common
- the skill has a nearby sibling with overlapping surface area
- a wrong-skill choice would waste time or produce misleading guidance

Keep it concise:

- name the neighboring skill or surface that should own the task
- explain the boundary in plain language
- avoid duplicating what the description already makes obvious unless the
  confusion is common in practice

### 2. Clear Output Expectations

Non-trivial skills should expose a stable output expectation, typically through
`Output Requirements` or `Output Contract`.

Use this when the skill regularly produces:

- reviewable structured guidance
- implementation summaries with repeated sections
- multi-step planning or validation output

Do not force identical section names across every skill. Consistency of intent
matters more than mechanical sameness.

### 3. Load References On Demand

Use `Load References On Demand` when the skill depends on deeper supporting
material.

Keep the list targeted:

- load references that materially affect decisions
- avoid long background-reading lists with low practical impact
- use a shared reference only when the skill actually participates in the
  shared convention being described

### 4. Anti-Patterns And Anti-Rationalization Notes

Use short anti-pattern sections only when the skill is especially vulnerable to
misclassification, unsafe defaults, or cargo-cult behavior.

Good candidates:

- customization or automation builders
- governance or process-heavy skills
- highly volatile targeted skills with recurring misuse patterns

Poor candidates:

- stable skills where the warnings would just restate the overview
- skills where misuse is already obvious from narrow scope and examples

### 5. Optional High-Volatility Disclosure Conventions

Conventions such as `OFFICIAL_CONFLICT` and `UNVERIFIED` are optional
high-volatility patterns, not universal catalog rules.

Use them for targeted skills where:

- official sources change quickly
- repo truth can materially diverge from latest stable guidance
- non-trivial recommendations can become misleading if uncertainty is hidden

Do not propagate them into stable shared skills by default.

### 6. Config-Aware Scaffolding

Use config-aware scaffolding when a skill owns a stable tool or project-config
surface and downstream adopters would benefit from a deterministic starter.

Core rule:

- real config files are the implementation source of truth
- Markdown references explain how to resolve and inspect config
- scaffold assets are optional starters, not silent policy overrides

Hosting model:

- keep the shared convention here in shared references
- keep actual scaffoldable config files and helper scripts inside the owning
  skill
- do not create one central cross-tool config bundle for unrelated tools

Use this pattern when:

- the skill regularly depends on concrete config files such as `ruff.toml`,
  `pyproject.toml` tool sections, `tsconfig.json`, `eslint.config.*`, or
  `.markdownlint.*`
- the repository already has a real config baseline or a clearly intentional
  strong-default starter profile
- a deterministic scaffold reduces repeated setup mistakes in downstream repos

Do not use this pattern when:

- the skill does not own a stable config surface
- the starter would be mostly speculative boilerplate
- the skill would have to silently install packages or rewrite CI to make the
  scaffold meaningful

Required behavior:

1. inspect repo-local config first when it exists
2. scaffold only when config is absent and the user wants the house style
3. report created versus skipped files deterministically
4. explain the next adaptation steps and validation command
5. keep dependency installation, task-runner wiring, and CI mutation explicit
   rather than automatic

Reference-writing rule:

- avoid restating the full live config policy in Markdown prose
- explain resolution order, entrypoints, common failure patterns, and
  adaptation points instead
- keep exact version/date snapshots in evidence or audits when they matter,
  not in evergreen skill references by default
- keep distributable skill references portable
- do not encode one repository's exact task names, target globs, ignore paths,
  or wrapper commands inside a shared skill unless the skill also owns a
  scaffolding mechanism that recreates that surface for adopters
- avoid shell-specific inspection snippets such as `sed`, `rg`, or Bash-only
  pipelines in portable references; describe what to inspect instead
- repository-specific live truth belongs in repo-root docs, config files, CI,
  and automation entrypoints; skill references should explain how to discover
  that truth

Portable-assumption rule:

- a distributable skill may assume only a small cross-platform baseline when
  that baseline is necessary for skill-owned assets or scaffolding to work
- acceptable assumptions are things like Python or Node/`npx` when the skill
  actually ships a helper or config for that ecosystem
- do not treat Bash, `Taskfile.yml`, `make`, `sed`, `rg`, or one repository's
  automation layout as part of the portable baseline
- if a skill needs more than the small portable baseline, document that
  dependency explicitly and keep repo-local wiring outside the skill bundle

### 7. Interactive Agent UX Baseline

Use this pattern for interactive custom agents that users invoke directly and
may need help discovering.

Good agent UX should make three things obvious:

1. what the agent is for
2. how a first-time user should start
3. where to get a short explanation versus deeper operational guidance

Preferred structure:

1. concise first-use orientation in the agent itself
2. a visible `help` / `how this works` path or equivalent handoff
3. a short quick-start/help surface for first-use onboarding
4. a deeper guide only when the workflow is rich enough to justify it

Use this pattern when:

- the agent supports a multi-step workflow
- the agent has handoffs or mode choices the user would not infer naturally
- the underlying skill is powerful but the first-use mental model is easy to
  miss

Do not use this pattern as:

- a forced long introduction on every invocation
- a substitute for the real skill or contract docs
- a reason to duplicate the same long explanation in agent, guide, and README

Required behavior:

1. keep the agent’s first-use framing short and action-oriented
2. make the help path visible in routing, arguments, or handoffs
3. keep the quick-start shorter than the deeper guide
4. let README-level discoverability stay concise instead of turning it into a
   full manual
5. explain lane or mode choices in plain language before using repo-specific
   jargon

### 8. Optional Adoption Bundles

Use this pattern when a skill has useful secondary adoption material that is
helpful for some repositories but should not bloat the main skill contract.

Good candidates:

- optional Task automation overlays
- optional hook bundles
- optional repo wiring examples that build on the skill's core assets

Core rule:

- keep the main `SKILL.md` lean
- keep optional adoption material in a dedicated reference such as
  `references/task-bundle.md`
- keep bundle files inside the owning skill's `assets/`
- treat bundle assets as source material the agent may help adopt, not as a
  default runtime dependency

Required behavior:

1. explain when the bundle should be used
2. explain when the bundle should be skipped
3. explain what files the bundle ships
4. explain how to reconcile with existing host-repo automation
5. avoid silently overwriting repo-global files such as root `Taskfile.yml`
6. avoid making installed skill paths part of the portable live contract

Reference-writing rule:

- do not let the optional bundle dominate the main skill narrative
- mention the bundle briefly in `SKILL.md`, then defer to the dedicated
  reference
- keep direct CLI or config-only adoption as the default fallback when the
  bundle is not adopted

## Authoring Guardrails

- Prefer selective normalization over catalog-wide schema forcing.
- Keep shared wording generic; keep domain detail local.
- Preserve strong local structures when they clearly serve the skill.
- Avoid adding sections just to match neighboring files.
- Include reasoning for non-obvious rules so future maintainers know why the
  convention exists.

## Source Notes

These conventions align with current official customization guidance that
emphasizes:

- short, self-contained instructions
- reasoning-backed non-obvious rules
- scoped specialization over giant uniform prompts

Primary references reviewed during Sprint 08:

- VS Code custom instructions:
  <https://code.visualstudio.com/docs/copilot/customization/custom-instructions>
- GitHub custom skills:
  <https://docs.github.com/copilot/how-tos/copilot-sdk/use-copilot-sdk/custom-skills>
- GitHub custom agents:
  <https://docs.github.com/en/copilot/how-tos/copilot-sdk/use-copilot-sdk/custom-agents>
