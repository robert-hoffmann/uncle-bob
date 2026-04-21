# Cross-Skill Authoring Conventions

Use this reference when shaping shared skill authoring patterns across the
catalog.

These conventions are selective, not universal. Apply them where they improve
routing, readability, or operator predictability. Do not force them into skills
where they become boilerplate.

## Shared Conventions Worth Reusing

### 1. Description-Writing As Routing Logic

Treat a skill description as routing metadata, not marketing copy.

Platform constraints to respect:

- keep the description comfortably below the `1024`-character hard limit from
  the Agent Skills spec
- remember that discovery reads only the skill `name` and `description`
- keep the description self-sufficient for routing because the body loads only
  after activation
- front-load the strongest user-intent and keyword triggers as a defensive
  authoring practice, even though order-sensitive ranking is not documented

Preferred pattern:

> Use this skill when the user wants X, Y, or Z; when the task involves A, B,
> or C; or when they ask for related outcomes even if they do not use the
> exact terminology. Do not use it for D or E.

Keep the emphasis on user intent first.

Good descriptions:

1. lead with what the user is trying to do
2. include adjacent phrasings the user might actually say
3. include an explicit non-use boundary only when misrouting is realistically
  common or costly
4. stay short enough to remain high-signal

Failure modes to avoid:

1. describing only what the skill contains instead of when to use it
2. relying on internal jargon the user is unlikely to say
3. omitting the non-use boundary entirely
4. writing something so broad that it competes with unrelated skills

### 2. Explicit "When Not To Use" Guidance

Use description-level non-use boundaries selectively, not mechanically.

Prefer them when:

- routing mistakes are realistically common
- the skill has a nearby sibling with overlapping surface area
- a wrong-skill choice would waste time or produce misleading guidance

Prefer body-level coordination guidance when:

- multiple skills should normally co-load
- the boundary depends on the task's primary concern rather than simple
  artifact presence
- a hard exclusion would suppress valid dual-layer loading

Add or strengthen a `When Not To Use` section when the description alone would
not make the boundary clear enough.

Keep it concise:

- name the neighboring skill or surface that should own the task
- explain the boundary in plain language
- avoid duplicating what the description already makes obvious unless the
  confusion is common in practice

For stack skills, prefer wording such as `co-load when overlap is normal; defer
only when the sibling clearly owns the primary concern`.

### 3. Clear Output Expectations

Non-trivial skills should expose a stable output expectation, typically through
`Output Requirements` or `Output Contract`.

Use this when the skill regularly produces:

- reviewable structured guidance
- implementation summaries with repeated sections
- multi-step planning or validation output

Do not force identical section names across every skill. Consistency of intent
matters more than mechanical sameness.

For high-impact skills, keep this section easy to find near the end of the
skill so readers can scan the expected reporting shape quickly without reading
the whole file first.

### 4. Examples Over Abstract Admonitions

Use examples when an abstract instruction could be followed in multiple ways.

Good examples:

1. show the desired output or wording pattern directly
2. stay short and close to the rule they clarify
3. include an anti-example only when misuse is likely

Avoid guidance like:

1. `follow best practices`
2. `write clear descriptions`
3. `improve the prompt`

Prefer guidance like:

1. `Use this skill when ... Do not use it for ...`
2. `Add one observable-outcome assertion beside the interaction assertion`
3. `Name the next action and one rejected alternative`

### 5. Load References On Demand

Use `Load References On Demand` when the skill depends on deeper supporting
material.

Keep the list targeted:

- load references that materially affect decisions
- avoid long background-reading lists with low practical impact
- use a shared reference only when the skill actually participates in the
  shared convention being described

### 6. Naming Conventions

For shared installable artifacts such as skills, prompts, and related guidance:

1. use lowercase, digits, and hyphens only when the host surface allows it
2. prefer short, verb-led or action-revealing names
3. keep names under 64 characters when practical
4. normalize titles into stable hyphen-case for installable artifacts

Do not introduce naming ceremony where the host surface does not actually use
or benefit from it.

### 7. Anti-Patterns And Anti-Rationalization Notes

Use short anti-pattern sections only when the skill is especially vulnerable to
misclassification, unsafe defaults, or cargo-cult behavior.

Good candidates:

- customization or automation builders
- governance or process-heavy skills
- highly volatile targeted skills with recurring misuse patterns

Poor candidates:

- stable skills where the warnings would just restate the overview
- skills where misuse is already obvious from narrow scope and examples

### 8. Optional High-Volatility Disclosure Conventions

Conventions such as `OFFICIAL_CONFLICT` and `UNVERIFIED` are optional
high-volatility patterns, not universal catalog rules.

Use them for targeted skills where:

- official sources change quickly
- repo truth can materially diverge from latest stable guidance
- non-trivial recommendations can become misleading if uncertainty is hidden

Do not propagate them into stable shared skills by default.

### 9. Config-Aware Scaffolding

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

### 10. Shared Choice-Question Contract

Use this pattern when a skill or related agent behavior asks the user to choose
between multiple options or paths.

Core rule:

- every multiple-choice prompt must preserve a custom or free-form reply path

Use this pattern when:

- the user is choosing between materially different implementation,
  planning, or workflow paths
- the agent needs a lightweight classification choice but still needs to allow
  a better custom answer
- the host exposes a question UI and the choice can be expressed cleanly there

Required behavior:

1. prefer `AskUserQuestion` / `vscode/askQuestions` or the equivalent host
   question UI when available
2. preserve a custom or free-form reply path for every multiple-choice prompt
3. keep the curated choice set to `2-4` plausible options when practical
4. mark the recommended option with `(*)` when a best fit exists
5. include a short explanation under every option in `(...)`
6. when the host question UI is unavailable, preserve the same structure in
   text with a final `Custom` option
7. use lightweight confirmations for simple confirmations and reserve the full
   option pattern for choices that materially change direction

Anti-patterns to avoid:

1. forcing the user into bare `A/B/C` or `1/2/3` replies with no custom path
2. listing every conceivable option instead of curating the most plausible
   choices
3. turning a simple confirmation into a bloated decision tree

Text fallback shape:

```text
Which path should we use?

`A` (*) recommended option
(Best fit because ...)

`B` alternative option
(Pros: ... Cons: ...)

`Custom`
```

### 11. Interactive Agent UX Baseline

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

1. keep the agent's first-use framing short and action-oriented
2. make the help path visible in routing, arguments, or handoffs
3. keep the quick-start shorter than the deeper guide
4. let README-level discoverability stay concise instead of turning it into a
   full manual
5. explain lane or mode choices in plain language before using repo-specific
   jargon

### 12. Optional Adoption Bundles

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
