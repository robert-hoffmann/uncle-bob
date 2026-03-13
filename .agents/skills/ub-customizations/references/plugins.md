# Agent Plugins Reference

## When to Use Plugins

Use a plugin **only** when the user wants:

- **Installability** — a team member can add the bundle in one step.
- **Internal team distribution** — shared via git repos or internal marketplaces.
- **Multi-component bundling** — skills, agents, prompts, hooks, MCP in one package.

Do NOT use plugins for:

- Local one-off customizations → use individual files
- Single-component needs → create the individual artifact directly
- Anything that does not require distribution or team sharing

**Rule**: Plugin packaging is an optional distribution layer, not a default. Only suggest it when distribution is explicitly requested.

## Plugin Format

**Manifest**: `plugin.json` at the plugin root.

**Status**: Agent plugins are a **preview feature**. Behavior may change.

## Plugin Manifest Structure

```json
{
  "name": "team-dev-workflows",
  "description": "Internal Copilot customizations for planning, testing, and release workflows",
  "version": "0.1.0",
  "skills": "skills/",
  "agents": "agents/",
  "hooks": "hooks.json",
  "mcpServers": ".vscode/mcp.json"
}
```

### Manifest Fields

| Field | Required | Description |
| --- | --- | --- |
| `name` | Yes | Plugin identifier. Lowercase, hyphens. |
| `description` | Yes | What the plugin provides. |
| `version` | Yes | Semantic version string. |
| `skills` | No | Path to skills directory. |
| `agents` | No | Path to agents directory. |
| `hooks` | No | Path to hooks JSON file. |
| `mcpServers` | No | Path to MCP config file. |

## Directory Structure

```text
my-plugin/
├── plugin.json
├── skills/
│   └── my-skill/
│       ├── SKILL.md
│       └── references/
├── agents/
│   ├── planner.agent.md
│   └── reviewer.agent.md
├── hooks.json
└── .vscode/
    └── mcp.json
```

## Distribution

### Git-Based Installation

Plugins are distributed via git repositories. Users install by adding the repo path to their VS Code settings:

```json
{
  "chat.plugins.paths": [
    "/path/to/local/plugin",
    "https://github.com/org/my-plugin.git"
  ]
}
```

### Local Development

For local development, point `chat.plugins.paths` to the local plugin directory.

## Extension vs Plugin Distinction

Do NOT conflate these two packaging layers:

| Aspect | Agent Plugin | VS Code Extension |
| --- | --- | --- |
| Format | `plugin.json` + files | `package.json` + extension code |
| Distribution | Git repos | VS Code Marketplace |
| Capabilities | Copilot customizations only | Full VS Code API access |
| Use when | Bundling Copilot-specific artifacts | Building full VS Code features |

Extensions can also contribute skills via `chatSkills` in their `package.json`. Only use this path when the user wants a standard VS Code extension with marketplace distribution.

## Common Plugin Contents

A useful plugin typically contains:

- One or more **skills** with references and scripts
- One or more **custom agents** with tool restrictions and handoffs
- **Prompt file** entry points for quick access
- **Hooks** for lifecycle automation
- **MCP config** for external capabilities

## Security Considerations

- **Review all hooks** — hooks execute shell commands and can be destructive.
- **Review MCP configs** — MCP servers have network access and may handle secrets.
- **Trust the source** — only install plugins from trusted repositories.
- **Audit regularly** — plugin behavior can change with git updates.
- Include a **security review note** with every generated plugin.

## Generation Checklist

- [ ] `plugin.json` at plugin root with name, description, version
- [ ] Clean directory structure with skills/, agents/, hooks
- [ ] All included components are individually valid
- [ ] Security review note included for hooks and MCP
- [ ] Install instructions documented (git URL or local path)
- [ ] No hardcoded secrets in any component
- [ ] Preview status noted — plugin system may evolve
