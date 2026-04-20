---
name: ub-customizations
description: >-
  Create, update, review, or refactor VS Code Copilot customizations — skills,
  prompt files, custom instructions, custom agents with handoffs, hooks, MCP
  server configs, or plugin bundles. Use when the user wants to build agent
  workflows, slash commands, lifecycle hooks, or multi-artifact combos, or
  needs help choosing which customization primitive fits their need.
argument-hint: "[what to build] [constraints]"
user-invocable: true
disable-model-invocation: false
---

# UB Customizations — VS Code Copilot Customization Builder

## Mission

Route the user to the correct VS Code Copilot customization primitive(s), generate safe and valid artifacts, validate output, and recommend companion artifacts when a single file is not enough.

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
  an existing stack rather than Copilot customization artifacts.

## Coordination

- Use `ub-customizations` to choose and generate the right customization
  primitive.
- Use `ub-authoring` when the task is about reusable cross-skill conventions
  such as routing-quality descriptions, non-use boundaries, naming, or shared
  authoring structure.
- Use both only when a customization task also changes the shared installable
  authoring contract.

## Artifact Selection Matrix

Classify the request BEFORE generating anything.

| User Need | Primary Artifact | Common Companions | Why |
| --- | --- | --- | --- |
| Project-wide conventions, architecture rules | Custom instructions | `AGENTS.md`, scoped `.instructions.md` | Always-on, low ceremony |
| Repetitive user-invoked one-step task | Prompt file | Optional custom agent | Best for slash-command workflows |
| Reusable multi-step capability with scripts/resources | Skill | Optional prompt file, instructions | On-demand domain workflows |
| Stable persona / role / tool policy / handoffs | Custom agent | Prompt file, skills | Roles, tool boundaries, guided workflows |
| Deterministic lifecycle automation | Hook | Custom agent, scripts | Guaranteed execution, not guidance |
| External systems, APIs, databases, browsers | MCP config | Skill, agent, prompt file | Real new capabilities via tools/resources |
| Shareable installable bundle | Plugin | Any of the above | Packaging layer, not behavior |

## Rules of Thumb

1. If it should be **always on** → instruction file.
2. If the user should **explicitly run it** and it is lightweight → prompt file.
3. If it is a **reusable capability bundle** with optional scripts/assets → skill.
4. If it needs a **persona, tool restrictions, subagents, or handoffs** → custom agent.
5. If it must **run deterministically** before/after lifecycle events → hook.
6. If it needs **real external capabilities/data** → MCP.
7. If the user wants to **ship/share/install** the whole thing → plugin.

**Always choose the smallest sufficient primitive.** Do not use a skill where an instruction file is enough. Do not use MCP where a local script is enough. Do not use a plugin where a repo-local folder is enough.

## Deep Classification Interview

Before generating anything, interview the user with targeted questions. Use `askQuestions` when available. Cover these areas — skip questions whose answers are already clear from context:

### Core Questions (always ask)

1. **What do you want to customize?** Describe the behavior, task, role, or automation you need.
2. **Should it always be active, or only when explicitly invoked?** (Always-on → instructions; invoked → prompt/skill/agent)
3. **Is it a one-step task or a multi-step workflow?** (One-step → prompt; multi-step → skill or agent)
4. **Does it need a specific persona, tool restrictions, or model preference?** (Yes → custom agent)
5. **Does it need guaranteed deterministic execution at specific lifecycle points?** (Yes → hook)
6. **Does it need access to external systems, APIs, or data sources?** (Yes → MCP)
7. **Should it be shareable or installable by other teams?** (Yes → plugin packaging)
8. **Do you need cross-vendor compatibility?** (Codex, Claude Code, Gemini CLI → export mode)

### Conditional Deep-Dive Questions (ask when relevant)

1. **Which tools should the agent/prompt have access to?** (When creating an agent or prompt with tool restrictions)
2. **What handoff stages does your workflow need?** (When creating a multi-phase agent: Plan → Implement → Review → Iterate)
3. **Which lifecycle events matter?** (When creating hooks: SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PreCompact, SubagentStart, SubagentStop, Stop)
4. **Would a multi-artifact bundle serve you better?** Recommend bundles when appropriate — see [references/bundles.md](references/bundles.md).

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
| **A** | Skill + Prompt file | Capability that should auto-activate AND be invocable via `/` |
| **B** | Agent + Prompt file | Persona/role with a shortcut entry point |
| **C** | Skill + MCP | Capability depending on external systems |
| **D** | Agent + Hook | Role agent needing guaranteed validation/automation |
| **E** | Instructions + Skill | Team conventions + on-demand domain procedures |
| **F** | Plugin | Multi-component distribution bundle |

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
| Custom instructions | [references/instructions.md](references/instructions.md) |
| Prompt files | [references/prompt-files.md](references/prompt-files.md) |
| Skills | [references/skills.md](references/skills.md) |
| Custom agents | [references/custom-agents.md](references/custom-agents.md) |
| Hooks | [references/hooks.md](references/hooks.md) |
| MCP configs | [references/mcp.md](references/mcp.md) |
| Plugins | [references/plugins.md](references/plugins.md) |
| Cross-vendor exports | [references/cross-vendor.md](references/cross-vendor.md) |

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
9. **Risks / follow-up** — preview features, secrets, plugin trust, unsupported vendor features
10. **Conflict note when relevant** — `OFFICIAL_CONFLICT` or `UNVERIFIED`
    with a concise explanation and the implementation consequence

## Completion Checklist

- Artifact choice is the smallest sufficient primitive for the request.
- Any recommended multi-artifact bundle is explained and justified.
- Generated files are valid for the chosen customization type.
- Tool access is least-privilege rather than broad by default.
- Validation and smoke-test guidance is explicit.
- VS Code-only versus broadly portable behavior is called out.
- Secret handling, trust, or preview-feature risks are surfaced when relevant.
- Any material official-source conflict or unverified non-trivial guidance is
  disclosed explicitly when relevant.

## Safety Defaults

- Default to **read-only planning** where possible.
- Default to **minimal tool sets** for generated agents.
- **Never hardcode** API keys, tokens, or secrets.
- Gate destructive actions behind **approval hooks** or confirmation.
- Include **review warnings** for hooks and MCP configs.
- Warn about **trust and security** when suggesting third-party skills, plugins, or MCP servers.

## Anti-Patterns to Avoid

- Do NOT default to a skill when an instruction file or prompt file is a better fit.
- Do NOT treat this skill as the owner of cross-catalog authoring conventions
  now that `ub-authoring` exists.
- Do NOT generate giant monolithic files — use progressive disclosure and references.
- Do NOT copy vendor-specific features (Claude `context: fork`, Gemini hook semantics) into VS Code outputs.
- Do NOT use hooks for soft guidance — hooks are for deterministic lifecycle actions.
- Do NOT use MCP for trivial local tasks — MCP is for real external capabilities.
- Do NOT grant all-tools access by default — use least privilege.
- Do NOT generate plugin packaging unless distribution is explicitly requested.

## Freshness Review

- Volatility: high
- Review recommendation: review on touch and during periodic maintenance, targeting a quarterly rhythm when practical.
- Trigger signals: VS Code Copilot customization-surface changes, new agent or hook capabilities, MCP schema changes, or portability model changes across supported vendors.
- Enforcement: advisory only; freshness warnings should not block unrelated customization work by default.
- Stable core: smallest-sufficient artifact choice, least privilege, and
  explicit validation remain the durable guidance even when platform features
  evolve quickly. Reusable authoring conventions now live in `ub-authoring`.
