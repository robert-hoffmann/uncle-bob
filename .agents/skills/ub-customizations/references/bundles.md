# Bundle Recommendations Reference

## Why Bundles Matter

Most real-world workflows need **multiple artifacts working together**. The builder should actively recommend bundles during classification rather than generating one artifact at a time.

## Bundle Matrix

### Bundle A: Skill + MCP

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

### Bundle B: Hook + helper script

**When to recommend**: Deterministic lifecycle automation needs logic that
should live outside a long inline shell command.

**Example scenario**: "Run a reviewable validation script after every edit and
block unsafe terminal commands before they execute."

- **Hook**: `PreToolUse` or `PostToolUse` hook definition.
- **Helper script**: small JS or Python wrapper that keeps the hook command
    portable and reviewable.

**File structure**:

```text
.github/hooks/post-tool-use.json
scripts/validate-after-edit.mjs
```

## Bundle Selection During Classification

When classifying the user's request, check if any bundle applies:

1. **Does the capability need external data or tools?** → Bundle A (Skill + MCP)
2. **Does deterministic lifecycle automation need reviewable logic outside the hook file?** → Bundle B (Hook + helper script)

If a bundle fits, recommend it proactively. Otherwise prefer a single artifact.

## Example Requests → Bundle Mapping

| User Request | Recommended Bundle |
| --- | --- |
| "Run ESLint after every edit" | B: Hook + helper script |
| "Connect Jira so agent can query tickets" | A: Skill + MCP |
| "Wrap a DB workflow around a reusable skill" | A: Skill + MCP |
| "Block destructive commands with a tested script" | B: Hook + helper script |
