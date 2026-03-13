# Bundle Recommendations Reference

## Why Bundles Matter

Most real-world workflows need **multiple artifacts working together**. The builder should actively recommend bundles during classification rather than generating one artifact at a time.

## Bundle Matrix

### Bundle A: Skill + Prompt File

**When to recommend**: The capability should both auto-activate when relevant AND be invocable explicitly via `/slash-command`.

**Example scenario**: "Teach Copilot how to run Playwright tests and let me invoke it directly."

- **Skill**: `SKILL.md` with testing workflow, references, and templates.
- **Prompt file**: `/run-playwright` entry point that routes to the skill.

**File structure**:

```text
.agents/skills/playwright-testing/
├── SKILL.md
└── references/
.github/prompts/run-playwright.prompt.md
```

### Bundle B: Custom Agent + Prompt File

**When to recommend**: The workflow needs a stable persona or tool policy, plus a quick shortcut entry point.

**Example scenario**: "Create a security review agent I can invoke with /review-security."

- **Agent**: `security-reviewer.agent.md` with restricted analysis tools.
- **Prompt file**: `/review-security` that routes to the agent.

**File structure**:

```text
.github/agents/security-reviewer.agent.md
.github/prompts/review-security.prompt.md
```

### Bundle C: Skill + MCP

**When to recommend**: The capability depends on external systems or remote data.

**Example scenario**: "Connect Jira so the agent can query tickets and create a workflow for managing issues."

- **Skill**: Issue management workflow with references.
- **MCP config**: `.vscode/mcp.json` for Jira connection.

**File structure**:

```text
.agents/skills/jira-issues/
├── SKILL.md
└── references/
.vscode/mcp.json
```

### Bundle D: Agent + Hook

**When to recommend**: A role-specific agent also needs guaranteed validation or automation at lifecycle points.

**Example scenario**: "I need a code review agent that automatically runs ESLint after every edit."

- **Agent**: `code-reviewer.agent.md` with analysis tools.
- **Hook**: PostToolUse hook running ESLint after file edits.

**File structure**:

```text
.github/agents/code-reviewer.agent.md
.github/hooks/post-tool-use.json
scripts/lint-after-edit.sh
```

### Bundle E: Instructions + Skill

**When to recommend**: There is a mix of always-on team conventions and on-demand domain procedures.

**Example scenario**: "Set up TypeScript strict mode rules for the whole repo, plus a skill for complex type migrations."

- **Instructions**: `.github/copilot-instructions.md` for always-on TS conventions.
- **Skill**: `ts-migration` skill for on-demand migration workflows.

**File structure**:

```text
.github/copilot-instructions.md
.agents/skills/ts-migration/
├── SKILL.md
└── references/
```

### Bundle F: Plugin (Multi-Component)

**When to recommend**: The user explicitly wants bundling, distribution, or installability.

**Example scenario**: "Package our planning, testing, and release workflows for the whole team."

- **Plugin**: Contains skills, agents, hooks, MCP config, and prompt entry points.

**File structure**:

```text
team-workflows/
├── plugin.json
├── skills/
│   ├── planning/SKILL.md
│   └── testing/SKILL.md
├── agents/
│   ├── planner.agent.md
│   └── reviewer.agent.md
├── hooks.json
└── .vscode/
    └── mcp.json
```

## Bundle Selection During Classification

When classifying the user's request, check if any bundle applies:

1. **Does the user want both auto-activation and explicit invocation?** → Bundle A (Skill + Prompt)
2. **Does the user want a persona/role with a quick entry point?** → Bundle B (Agent + Prompt)
3. **Does the capability need external data/tools?** → Bundle C (Skill + MCP) or add MCP to any bundle
4. **Does a role agent need lifecycle guarantees?** → Bundle D (Agent + Hook)
5. **Are there both conventions and procedures?** → Bundle E (Instructions + Skill)
6. **Is distribution or team sharing needed?** → Bundle F (Plugin)

If a bundle fits, recommend it proactively. Generate all components together.

## Example Requests → Bundle Mapping

| User Request | Recommended Bundle |
| --- | --- |
| "Always use pnpm and strict TS" | No bundle — just instructions |
| "Create /review-security for dependency review" | B: Agent + Prompt (or just Prompt if simple) |
| "Teach Copilot Playwright testing with templates" | A: Skill + Prompt |
| "Planning agent that never edits code" | B: Agent + Prompt + Handoff to implementer |
| "Run ESLint after every edit" | No bundle — just a hook |
| "Connect Jira so agent can query tickets" | C: Skill + MCP |
| "Ship workflow tools for the team" | F: Plugin |
| "Set TS rules + complex migration helper" | E: Instructions + Skill |
