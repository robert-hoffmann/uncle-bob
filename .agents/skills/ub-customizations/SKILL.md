---
name: ub-customizations
description: >-
  Create, update, review, or refactor VS Code Copilot skills, hooks, and MCP
  configs. Use when the user wants to build or maintain reusable skills,
  lifecycle hooks, MCP integrations, or the supporting references and
  validation flow around those artifacts, or needs help deciding between a
  skill, hook, or MCP config.
argument-hint: "[what to build] [constraints]"
user-invocable: true
disable-model-invocation: false
---

# UB Customizations — VS Code Copilot Customization Builder

## Mission

Route the user to the correct VS Code Copilot artifact within this skill's
scope, generate safe and valid skills, hooks, or MCP configs, validate output,
and recommend companion artifacts only when they materially improve the
workflow.

Implement against the target host and tool reality, but bias the generated
customization toward current official guidance and forward-compatible artifact
choices instead of preserving deprecated or legacy customization surfaces by
default.

## When Not To Use

- Do not use this skill for general repository workflow planning; defer that to
  `ub-workflow`.
- Do not use this skill for governance-only policy or evidence questions;
  defer those to `ub-governance`.
- Do not use this skill as the owner of reusable cross-skill authoring
  conventions; defer those to `ub-authoring`.
- Do not use this skill when the user only needs normal code implementation in
  an existing stack rather than skill, hook, or MCP artifacts.

## Coordination

- Use `ub-customizations` as the default builder workflow for skills, hooks,
  and MCP configs.
- Use `ub-authoring` when the task is about reusable cross-skill conventions
  such as routing-quality descriptions, non-use boundaries, naming, or shared
  authoring structure.
- Use both only when a customization task also changes the shared installable
  authoring contract.

## Artifact Selection Matrix

Classify the request BEFORE generating anything.

| User Need | Primary Artifact | Common Companions | Why |
| --- | --- | --- | --- |
| Reusable multi-step capability with scripts/resources | Skill | Optional MCP config | On-demand domain workflow with bundled references, scripts, or assets |
| Deterministic lifecycle automation | Hook | Optional helper script | Guaranteed execution at agent lifecycle points; not soft guidance |
| External systems, APIs, databases, browsers | MCP config | Optional skill | Real new capabilities via tools/resources and authenticated external access |
| Everything else | Out of scope here | See other customization primitives directly | Instructions, prompt files, custom agents, and plugin packaging are no longer first-class scope for this skill |

## Rules of Thumb

1. If it is a **reusable multi-step capability** with references, scripts, or
  assets → skill.
2. If it must **run deterministically** before or after lifecycle events →
  hook.
3. If it needs **real external capabilities, tools, or data** outside the
  workspace → MCP.
4. If a skill depends on external systems, pair the skill with MCP instead of
  overloading the skill alone.
5. Always choose the smallest sufficient artifact inside this skill's scope.
6. Do not use MCP where a local script is enough.
7. Do not use a hook for soft guidance when a skill is the real fit.

**Always choose the smallest sufficient artifact inside this skill's scope.**

## Deep Classification Interview

Before generating anything, interview the user with targeted questions. Use
`askQuestions` when available, and follow the shared `ub-authoring`
choice-question contract for any multiple-choice prompts. Skip questions whose
answers are already clear from context.

### Core Questions (always ask)

1. **What do you want to build or change?** Describe the behavior, workflow,
  automation, or integration you need.
2. **Is this a reusable on-demand workflow, a deterministic lifecycle action,
  or an external integration?**
3. **Does it need to run automatically at specific lifecycle points?** If yes,
  which events matter?
4. **Does it need access to external systems, APIs, databases, browsers, or
  remote data sources?**
5. **Does it need bundled references, scripts, or assets to guide repeated
  use?**

### Conditional Deep-Dive Questions (ask when relevant)

1. **Which lifecycle events matter?** Use the VS Code hook events when a hook
  is in scope.
2. **Which external systems, credentials, transports, or trust boundaries
  matter?** Use this when MCP is in scope.
3. **Would a companion artifact materially improve the workflow?** Recommend
  Skill + MCP when the skill depends on external systems.

After classification, state the recommendation, assumptions, and rationale before generating.

## Platform & Research Policy

- Treat the latest stable VS Code and GitHub Copilot customization guidance as
  the preferred baseline for artifact choice, file structure, and capability
  recommendations.
- Detect workspace and host truth before generating: repository structure,
  existing customization artifacts, target host, available tools, and
  portability requirements.
- Treat repo and host truth as the gold implementation standard when deciding
  what can actually ship safely in the target environment.
- Use web search to verify current official customization guidance against
  primary VS Code and GitHub documentation before making non-trivial or
  platform-sensitive recommendations.
- If official guidance and repo or host truth diverge materially on a
  non-trivial recommendation, surface `OFFICIAL_CONFLICT`, implement the
  host-safe path, and explain the migration or portability consequence.
- If official sources disagree with each other on a non-trivial
  recommendation, also surface `OFFICIAL_CONFLICT` instead of silently
  collapsing the disagreement.
- If a non-trivial claim cannot be confirmed in official sources after
  targeted research, mark it `UNVERIFIED` or avoid presenting it as settled
  guidance.
- Keep conflict and uncertainty disclosure scoped to non-trivial,
  platform-sensitive, or contested guidance rather than simple artifact
  generation.

## Bundle Recommendations

Many workflows need multiple artifacts working together. Actively recommend these bundles during classification:

| Bundle | Components | When to Recommend |
| --- | --- | --- |
| **A** | Skill + MCP | The workflow is reusable but depends on external systems, authenticated tools, or remote data |
| **B** | Hook + helper script | Deterministic lifecycle automation needs logic that should live outside inline shell |

For detailed bundle guidance and example scenarios, read [references/bundles.md](references/bundles.md).

## Generation Workflow

Follow these steps in order:

### 1. Classify

Parse the request. Identify the artifact type(s) needed using the selection matrix above.

### 2. Interview

Ask classification questions. Confirm the chosen artifact type(s) with the user.

### 3. Plan

State assumptions, file tree, and rationale. For the artifact type being generated, load the appropriate reference:

| Artifact Type | Reference to Load |
| --- | --- |
| Skills | [references/skills.md](references/skills.md) |
| Hooks | [references/hooks.md](references/hooks.md) |
| MCP configs | [references/mcp.md](references/mcp.md) |

For customization-artifact writing guidance, read
[references/prompt-engineering.md](references/prompt-engineering.md).
For reusable cross-skill authoring conventions, read
[`../ub-authoring/references/authoring-conventions.md`](../ub-authoring/references/authoring-conventions.md).

Before generating non-trivial or platform-sensitive customizations, compare
official guidance, repo truth, and target host reality and surface
`OFFICIAL_CONFLICT` or `UNVERIFIED` when relevant.

### 4. Generate

Create the files following the loaded reference. Apply these defaults:

- **Shared authoring contract**: rely on `ub-authoring` for reusable naming,
  routing, and shared structure conventions.
- **Least privilege**: expose only necessary tools; minimize dangerous defaults.
- **No hardcoded secrets**: use MCP `inputs`, environment variables, or `.env` references.
- **Concise descriptions**: optimize for triggering and discovery, not marketing.

### 5. Validate

Run the validation checklist from [references/validation.md](references/validation.md) for each generated artifact. Produce:

- Validation checklist (pass/fail per item)
- Smoke-test prompts (how to test the artifact)
- Portability notes (VS Code-only vs Copilot-compatible vs broadly portable)

### 6. Iterate

Present the output for review. Refine based on user feedback. Re-validate after changes.

## Output Contract

Treat this section as the stable output expectation for non-trivial
customization work in this catalog.

Structure every generation response as:

1. **Recommendation** — what to generate and why
2. **Source truth note** — detected host, repo artifact reality, and any
   material gap versus latest official guidance
3. **Assumptions** — defaults chosen, unresolved ambiguities
4. **File tree** — directories and files to create or update
5. **Generated content** — file-by-file output
6. **Validation checklist** — human review items + technical checks
7. **Smoke-test prompts** — how to verify the artifact works
8. **Portability notes** — which pieces are VS Code-only, Copilot-compatible, or broadly portable
9. **Risks / follow-up** — preview features, secrets, trust, unsupported host features
10. **Conflict note when relevant** — `OFFICIAL_CONFLICT` or `UNVERIFIED`
    with a concise explanation and the implementation consequence

## Completion Checklist

- Artifact choice is the smallest sufficient primitive for the request.
- Any recommended multi-artifact bundle is explained and justified.
- Generated files are valid for the chosen customization type.
- Tool access is least-privilege rather than broad by default.
- Validation and smoke-test guidance is explicit.
- VS Code-only versus Agent-Skills-portable behavior is called out.
- Secret handling, trust, or preview-feature risks are surfaced when relevant.
- Any material official-source conflict or unverified non-trivial guidance is
  disclosed explicitly when relevant.

## Safety Defaults

- Default to **read-only planning** where possible.
- Default to **minimal scopes** for generated hooks and MCP servers.
- **Never hardcode** API keys, tokens, or secrets.
- Gate destructive actions behind **approval hooks** or confirmation.
- Include **review warnings** for hooks and MCP configs.
- Warn about **trust and security** when suggesting third-party skills or MCP servers.

## Anti-Patterns to Avoid

- Do NOT default to a skill when a hook or MCP config is the real fit.
- Do NOT treat this skill as the owner of cross-catalog authoring conventions
  now that `ub-authoring` exists.
- Do NOT generate giant monolithic files — use progressive disclosure and references.
- Do NOT use hooks for soft guidance — hooks are for deterministic lifecycle actions.
- Do NOT use MCP for trivial local tasks — MCP is for real external capabilities.
- Do NOT grant broad tool or secret access by default — use least privilege and explicit inputs.

## Freshness Review

- Volatility: high
- Review recommendation: review on touch and during periodic maintenance, targeting a quarterly rhythm when practical.
- Trigger signals: VS Code Copilot skill, hook, or MCP surface changes; Agent Skills spec changes; MCP schema changes; lifecycle-event changes; or portability guidance changes tied to the official Agent Skills spec.
- Enforcement: advisory only; freshness warnings should not block unrelated customization work by default.
- Stable core: smallest-sufficient artifact choice, least privilege, explicit
  validation, and the builder-versus-authoring ownership split remain the
  durable guidance.
