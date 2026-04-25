# UB Customizations

Source: `.agents/skills/ub-customizations/SKILL.md`

`ub-customizations` helps choose and build reusable agent customization
artifacts: skills, hooks, MCP configs, prompts, bundles, and validation
surfaces.

## Core Principles

- Classify the artifact before generating it.
- Choose the smallest customization surface that solves the problem.
- Separate reusable guidance from deterministic automation.
- Use interviews when artifact choice materially changes the result.
- Keep secrets and environment-specific values outside generated artifacts.
- Validate generated skills, hooks, MCP configs, and bundles with the
  appropriate checklist.

## Behavior In Practice

- Classifies the request before generating files: skill for reusable on-demand
  guidance, hook for deterministic lifecycle automation, MCP config for real
  external capabilities, and bundle only when multiple artifacts materially
  improve the workflow.
- Interviews only for unresolved path-changing facts: automatic lifecycle
  events, external systems, credentials, bundled references, host portability,
  and companion artifacts.
- Treats hooks as automation, not advice. If the user needs guaranteed
  behavior before or after agent lifecycle events, the skill prefers a hook
  plus a small helper script over a long inline shell command.
- Treats MCP as capability expansion. If the workflow needs authenticated APIs,
  databases, browsers, remote services, or tools outside the workspace, it
  designs explicit transports, inputs, names, and trust boundaries.
- Keeps skills lean with progressive disclosure: the main `SKILL.md` routes
  and orchestrates, while references, scripts, or assets carry detail only
  when they are needed.
- Applies least privilege by default: narrow tools, no hardcoded secrets,
  explicit environment or input variables, and warnings for preview features
  or third-party trust.
- Validates generated artifacts with smoke-test prompts and portability notes
  so users know whether a customization is VS Code-specific, Copilot-specific,
  or broadly portable.

## Reference Highlights

- `.agents/skills/ub-customizations/references/skills.md`: skill anatomy,
  metadata, routing descriptions, progressive disclosure, bundled references,
  scripts, assets, and generation checklist.
- `.agents/skills/ub-customizations/references/hooks.md`: hook events,
  file structure, deterministic automation examples, wrapper-script defaults,
  destructive-command guardrails, and preview-status warnings.
- `.agents/skills/ub-customizations/references/mcp.md`: MCP server config,
  stdio versus HTTP transport choices, secret inputs, sandbox support,
  capability naming, and generation defaults.
- `.agents/skills/ub-customizations/references/bundles.md`: when to combine
  skills, hooks, MCP configs, and helper scripts without building a monolith.
- `.agents/skills/ub-customizations/references/validation.md`: artifact
  validation checklists, trigger-evaluation prompts, MCP and hook smoke tests,
  and human review questions.
- `.agents/skills/ub-customizations/references/prompt-engineering.md`:
  instruction structure, routing-description formula, examples-over-advice,
  tool guidance rules, progress patterns, and naming conventions.

## Progressive Disclosure

The main skill performs classification and high-level workflow. It loads the
artifact-specific reference only after the artifact type is clear: skills for
skill generation, hooks for lifecycle automation, MCP for external tools, and
validation for final review.

## Common Invocation Examples

- “Use `ub-customizations` to decide whether this should be a skill or hook.”
- “Create a skill for this reusable workflow.”
- “Review this MCP config and companion skill design.”
- “Package this as a bundle with validation guidance.”

## Boundaries

Do not use it for general code implementation or governance-only decisions.
Use `ub-authoring` when the work is only reusable wording, routing quality, or
shared authoring convention cleanup.

## Tradeoffs

Strength: prevents overbuilding customization systems and keeps artifact
choice explicit.

Cost: classification can require an interview before implementation when the
right artifact is not obvious.
