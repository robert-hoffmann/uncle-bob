---
name: ub-customize
description: >-
  Create or update VS Code Copilot customizations: skills, prompt files, custom
  agents, instructions, hooks, MCP configs, plugins, or multi-artifact bundles.
argument-hint: "[what to create or update] [target platform] [constraints]"
agent: ub-customizations
---

# UB Customize

Use the `ub-customizations` custom agent for this request.

Interpret any text after `/ub-customize` as the customization request.

Behavior:

- **No argument**: present the available customization types and ask what the user wants to create.
- **Argument provided**: classify the request and begin the customization workflow.

Available customization types:

- `instruction` — always-on repo-wide or scoped coding conventions
- `prompt` — user-invoked slash command for a specific task
- `skill` — reusable multi-step capability bundle with scripts/references
- `agent` — persistent persona with tool restrictions, handoffs, or subagents
- `hook` — deterministic lifecycle automation (lint, block, validate, log)
- `mcp` — external tool/data integration via MCP server config
- `plugin` — installable multi-component bundle for team distribution
- `bundle` — multi-artifact combo (skill+prompt, agent+hook, etc.)
