# Hooks Reference

## When to Use Hooks

Use hooks when deterministic lifecycle automation is required — behavior that **must run no matter what** before or after specific events. Hooks are for **enforcement**, not guidance.

**Good use cases:**

- Run Prettier or ESLint after file edits
- Block destructive shell commands
- Require approval before infrastructure changes
- Log every tool invocation
- Inject project context when sessions start
- Run tests after code generation
- Audit trail recording

**Do NOT use hooks for:**

- General style guidance → use instructions
- Occasional user-invoked workflows → use prompt files or skills
- Domain expertise → use skills
- External system integration → use MCP

## Hook Events

VS Code supports 8 lifecycle events:

| Event | When It Fires | Common Use |
| --- | --- | --- |
| `SessionStart` | Chat session begins | Context injection, environment setup |
| `UserPromptSubmit` | User sends a message | Prompt transformation, context augmentation |
| `PreToolUse` | Before a tool executes | Block dangerous tools, require approval |
| `PostToolUse` | After a tool executes | Lint/format after edits, validation |
| `PreCompact` | Before context compaction | Save important context |
| `SubagentStart` | Before a subagent runs | Audit, context injection |
| `SubagentStop` | After a subagent completes | Validation, logging |
| `Stop` | Agent completes its turn | Final validation, summary generation |

## File Format

**Location**: `.github/hooks/<event-name>.json` or `.github/hooks/hooks.json` (combined).

### Single-Event Hook

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "type": "command",
        "command": "./scripts/run-eslint-on-edits.sh",
        "timeout": 30
      }
    ]
  }
}
```

### Multi-Event Hook

```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "cat .github/session-context.md",
        "timeout": 10
      }
    ],
    "PreToolUse": [
      {
        "type": "command",
        "command": "./scripts/block-destructive.sh",
        "timeout": 5,
        "toolNames": ["runCommand"]
      }
    ],
    "PostToolUse": [
      {
        "type": "command",
        "command": "./scripts/lint-after-edit.sh",
        "timeout": 30,
        "toolNames": ["editFiles", "createFile"]
      }
    ]
  }
}
```

### Hook Fields

| Field | Required | Description |
| --- | --- | --- |
| `type` | Yes | Always `"command"` for VS Code hooks. |
| `command` | Yes | Shell command or script path to execute. |
| `timeout` | No | Max execution time in seconds. Default conservatively (10-30s). |
| `toolNames` | No | Filter — only fire for specific tool names (PostToolUse, PreToolUse). |

### Agent-Scoped Hooks (Preview)

Custom agents can define hooks in their frontmatter:

```yaml
hooks:
  PostToolUse:
    - type: command
      command: "./scripts/validate.sh"
      timeout: 15
```

**Warning**: Agent-scoped hooks are a preview feature. Behavior may change.

## Example Patterns

### Pattern 1: Lint After Edits

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "type": "command",
        "command": "npx eslint --fix ${TOOL_OUTPUT_FILE:-}",
        "timeout": 30,
        "toolNames": ["editFiles", "createFile"]
      }
    ]
  }
}
```

### Pattern 2: Block Destructive Commands

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "type": "command",
        "command": "./scripts/block-destructive.sh",
        "timeout": 5,
        "toolNames": ["runCommand"]
      }
    ]
  }
}
```

Example `scripts/block-destructive.sh`:

```bash
#!/bin/bash
# Block dangerous commands — exit non-zero to prevent execution
BLOCKED_PATTERNS="rm -rf|drop table|truncate|format c:|del /f"
if echo "$TOOL_INPUT" | grep -qiE "$BLOCKED_PATTERNS"; then
  echo "BLOCKED: Destructive command detected. Requires manual approval."
  exit 1
fi
```

### Pattern 3: Session Context Injection

```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "cat .github/session-context.md",
        "timeout": 10
      }
    ]
  }
}
```

### Pattern 4: Test Validation After Generation

```json
{
  "hooks": {
    "Stop": [
      {
        "type": "command",
        "command": "npm test -- --passWithNoTests",
        "timeout": 60
      }
    ]
  }
}
```

## Generation Defaults

- Prefer **small wrapper scripts** over giant inline shell one-liners.
- Set **conservative timeouts** (10-30 seconds for most hooks).
- Add **comments** about expected stdin/stdout behavior.
- Make destructive blocks **explicit and reviewable**.
- For approval hooks, default to **"ask" instead of silent allow** for sensitive operations.
- Include a **README or inline comments** explaining what each hook does.

## Preview Status Warning

VS Code hook support is simpler than Claude/Gemini hook systems. Treat VS Code hooks as **command-driven lifecycle automation**, not a rich generalized agent framework. Some features (agent-scoped hooks, advanced event data) are in preview and may change.

## Generation Checklist

- [ ] File location: `.github/hooks/` directory
- [ ] Correct event type chosen for the use case
- [ ] `type: "command"` specified
- [ ] Command is small and reviewable
- [ ] Conservative timeout set
- [ ] `toolNames` filter applied when hook is tool-specific
- [ ] Helper scripts are executable and tested
- [ ] No hardcoded secrets in commands
- [ ] Destructive blocks are explicit, not silent
- [ ] Preview features noted where applicable
