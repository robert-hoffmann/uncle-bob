# Prompt Files Reference

## When to Use Prompt Files

Use a prompt file when the task is **explicit, user-invoked, and relatively lightweight**. Prompt files act as slash commands — the user types `/name` to run them.

Do NOT use prompt files for:

- Always-on guidance → use instructions
- Multi-step capability bundles with scripts/resources → use skills
- Persistent personas with tool restrictions → use custom agents
- Deterministic automation → use hooks

## File Format

**Location**: `.github/prompts/*.prompt.md` or user profile prompts folder.

**Structure**: YAML frontmatter + Markdown body.

### Frontmatter Fields

| Field | Required | Description |
| --- | --- | --- |
| `name` | Yes | Display name shown in the prompt picker. Keep short and action-oriented. |
| `description` | Yes | Explains what the prompt does. Shown in the prompt picker. |
| `argument-hint` | No | Placeholder text shown in the chat input after typing the prompt name. |
| `agent` | No | Routes the prompt to a specific custom agent. |
| `model` | No | Pins the prompt to a specific model (e.g., `claude-sonnet-4`). |
| `tools` | No | Array of tool names the prompt can use. **Overrides agent tools if both are set.** |

### Important: Tool Override Rule

If both a prompt file and its target custom agent define `tools`, the **prompt file's tool list wins**. Only specify prompt-level tools if you intentionally want to override the agent's defaults.

## Template

```markdown
---
name: review-security
description: Review code for security issues and risky patterns.
argument-hint: "[scope or files]"
agent: agent
tools: ["search", "read/problems", "search/changes"]
---

Review the requested scope for:
- auth/session issues
- secrets exposure
- injection risks
- unsafe dependency usage

Return:
1. Findings
2. Severity
3. Concrete fixes
4. Tests or checks to run
```

## Body Guidelines

The body is the prompt that gets sent to the agent. It should:

- Start with the task clearly stated.
- Specify **inputs, outputs, and constraints**.
- Break down complex work into steps.
- Include **acceptance criteria** or expected output format.
- Avoid vague verbs like "improve" without defining what "improve" means.
- Tell the model **when to ask questions** vs proceed autonomously.

## Prompt File vs Skill Decision

| Factor | Prompt File | Skill |
| --- | --- | --- |
| Complexity | One-step or simple multi-step | Rich multi-step with scripts/resources |
| Resources | No bundled files | Scripts, references, assets |
| Activation | User-invoked only | User-invoked or model-triggered |
| Portability | VS Code specific | Open standard (agentskills.io) |
| Context cost | Low (single file) | Higher (SKILL.md + optional resources) |

**Rule of thumb**: If the task fits in one file with no bundled resources, use a prompt file. If it needs scripts, references, or rich procedural guidance, use a skill.

## Routing to Custom Agents

A prompt file can route to a custom agent via the `agent` field:

```markdown
---
name: ub-governance
description: Interactive governance help and topic routing.
argument-hint: "overview | evidence | testing | repository"
agent: ub-governance
---

Use the ub-governance agent for this request.
Interpret text after /ub-governance as the topic.
```

This creates a quick entry point (`/ub-governance`) that delegates to a richer agent persona.

## Generation Checklist

- [ ] File location: `.github/prompts/<name>.prompt.md`
- [ ] Valid frontmatter: `name` and `description` present
- [ ] `argument-hint` provided if the prompt accepts arguments
- [ ] `agent` field set if routing to a custom agent
- [ ] `tools` only specified if intentionally overriding agent tools
- [ ] Body specifies task, constraints, and output format
- [ ] Body uses acceptance criteria, not vague instructions
- [ ] No hardcoded secrets or sensitive data
