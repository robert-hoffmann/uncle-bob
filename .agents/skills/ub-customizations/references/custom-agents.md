# Custom Agents Reference

## When to Use Custom Agents

Use a custom agent when the workflow needs a **persistent persona, tool restrictions, model preferences, subagent access, or handoffs**. Agents are better than skills for roles, tool boundaries, and guided multi-phase workflows.

Do NOT use custom agents for:

- Always-on guidance → use instructions
- Simple one-step tasks → use prompt files
- Reusable capability bundles without persona needs → use skills
- Deterministic automation → use hooks

## File Format

**Location**: `.github/agents/<name>.agent.md` or user profile agents folder.

**Structure**: YAML frontmatter + Markdown body.

## Frontmatter Fields

| Field | Required | Description |
| --- | --- | --- |
| `name` | Yes | Display name for the agent. |
| `description` | Yes | Explains the agent's purpose and expertise. |
| `tools` | No | Array of tool names the agent can access. Restricts the tool set. |
| `agents` | No | Array of subagent names this agent can delegate to. |
| `model` | No | Pin to a specific model (e.g., `claude-sonnet-4`). |
| `handoffs` | No | Array of handoff buttons for multi-phase workflows. |
| `hooks` | No | Agent-scoped hooks (preview). |
| `target` | No | Execution target: `agent` (Copilot) or `terminal` (CLI). |
| `mcp-servers` | No | MCP servers available to this agent (GitHub Copilot target context). |
| `user-invocable` | No | Set `true` for direct user invocation. |
| `disable-model-invocation` | No | Set `true` to prevent auto-activation. |
| `argument-hint` | No | Placeholder text shown when invoked. |

## Tool Restriction

Specify only the tools the agent needs. Common tool categories:

- **Read-only**: `codebase`, `search`, `usages`, `read/readFile`, `read/problems`
- **Editing**: `editFiles`, `createFile`
- **Execution**: `runCommand`, `runTask`
- **VS Code**: `vscode` (askQuestions, openFile, etc.)
- **Web**: `web`, `fetch`
- **Subagents**: `agent`
- **MCP**: `<server-name>/*` (all tools from an MCP server)

**Least privilege**: only expose tools the agent actually needs. Avoid `["*"]` or leaving tools unspecified for sensitive roles.

## Handoffs

Handoffs are buttons that transition between workflow phases. They are one of the most valuable surfaces for multi-stage workflows.

### Handoff Structure

```yaml
handoffs:
  - label: "Implement Plan"
    agent: agent
    prompt: "Implement the approved plan above."
    send: false
  - label: "Review Code"
    agent: code-reviewer
    prompt: "Review the implementation for quality and security."
    send: false
```

### Handoff Fields

| Field | Description |
| --- | --- |
| `label` | Button text — describe the next action, not generic navigation. |
| `agent` | Target agent name. Can be `agent` (default Copilot) or a custom agent. |
| `prompt` | Continuation context for the next phase. Keep minimal but concrete. |
| `send` | `false` (default — safer) lets user review before sending. `true` auto-sends. |
| `model` | Optional model override for the next phase. |

### Handoff Design Rules

- Labels should describe the **next action**: "Implement Plan", "Run Tests", "Review Security".
- Prompts should carry **minimal but concrete continuation context**.
- Default `send: false` — let the user review before proceeding.
- Use model overrides only when the next phase genuinely benefits from a different model.
- Good handoffs feel like **workflow buttons**, not generic navigation.

### Common Handoff Patterns

- **Plan → Implement**: Planner creates plan, hands off to implementer.
- **Implement → Review**: Implementer finishes, hands off to reviewer.
- **Write Tests → Implement Code**: Test-driven development flow.
- **Investigate → Patch**: Research agent finds the issue, hands off to fixer.
- **Audit → Fix**: Security/quality audit leads to remediation.

## Subagent Design

### When to Use Subagents

Use subagents or agent delegation when:

- Research should be **isolated from the main thread**.
- A **specialist role** is needed with restricted tools.
- Planning and implementation should **not share the same context**.
- Review should be **independent from authoring**.

### Recommended Three-Agent Pattern

For teams needing structured workflows, scaffold this common pattern:

#### 1. Planner Agent

- Read-only tools: `codebase`, `search`, `usages`, `fetch`
- Creates implementation plan
- Hands off to implementer

#### 2. Implementer Agent

- Editing tools: `editFiles`, `createFile`, `runCommand`
- Executes the plan
- Hands off to reviewer

#### 3. Reviewer Agent

- Analysis tools: `search`, `problems`, `usages`
- Security and quality focus
- Optionally hands back fix suggestions

### Subagent Access

Use the `agents` field to allow an agent to delegate to specific subagents:

```yaml
agents: ["explorer", "security-reviewer"]
```

Only list agents the parent actually needs to delegate to.

## Template: Role Agent with Handoffs

```markdown
---
name: Planner
description: Create implementation plans without making code changes.
tools: ["fetch", "search", "usages", "githubRepo"]
handoffs:
  - label: Implement Plan
    agent: agent
    prompt: Implement the approved plan above.
    send: false
---

# Planning Instructions

- Research before proposing.
- Do not modify files.
- Produce a step-by-step plan with verification tasks.
```

## Template: Specialist Agent with Tool Restrictions

```markdown
---
name: security-reviewer
description: Review code for security vulnerabilities and risky patterns.
tools: ["codebase", "search", "problems", "usages"]
user-invocable: true
disable-model-invocation: true
---

# Security Review Instructions

## Mission
Identify security vulnerabilities, risky patterns, and unsafe defaults.

## Focus Areas
- Authentication and authorization flaws
- Injection vulnerabilities (SQL, XSS, command injection)
- Secret exposure
- Unsafe dependencies
- Missing input validation at system boundaries
```

## Body Guidelines

The agent body is loaded when the agent is selected. It should contain:

1. **Identity / role** — who is this agent?
2. **Mission** — what is the primary goal?
3. **Constraints / boundaries** — what should the agent NOT do?
4. **Procedure / workflow** — step-by-step guidance.
5. **Tool guidance** — when and how to use available tools.
6. **Source of truth** — reference files or skills to load on demand.

## Generation Checklist

- [ ] File location: `.github/agents/<name>.agent.md`
- [ ] Valid frontmatter: `name` and `description` present
- [ ] `tools` list follows least privilege — only needed tools
- [ ] `handoffs` have descriptive labels and `send: false` by default
- [ ] `agents` list only includes actually needed subagents
- [ ] Body follows role/mission/constraints/procedure structure
- [ ] No hardcoded secrets or sensitive data
- [ ] Source of truth references are correct paths
