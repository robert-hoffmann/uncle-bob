# Cross-Vendor Compatibility Reference

## Compatibility Modes

The builder supports three compatibility modes. Default to **vscode-strict** unless the user requests otherwise.

### Mode A: `vscode-strict` (Default)

Generate only what is clearly valid for VS Code Copilot. Use when the user says nothing about other platforms.

### Mode B: `copilot-portable`

Generate outputs compatible with:

- VS Code Copilot
- GitHub Copilot CLI
- GitHub Copilot coding agent

Minimal divergence — use open standards where possible.

### Mode C: `cross-vendor-export`

Generate the VS Code target **plus** optional companion exports for:

- Codex (AGENTS.md / CODEX.md)
- Claude Code (CLAUDE.md / .claude/ directory)
- Gemini CLI (GEMINI.md / custom commands)
- Cursor (best-effort, verify before shipping)

## Vocabulary Map Across Ecosystems

| Concept | VS Code / Copilot | Copilot CLI | Codex | Claude Code | Gemini CLI |
| --- | --- | --- | --- | --- | --- |
| Always-on guidance | `AGENTS.md`, optional `copilot-instructions.md`, `.instructions.md`, `CLAUDE.md` | `AGENTS.md`, `Copilot.md`, `GEMINI.md`, `CODEX.md` | `AGENTS.md` | `CLAUDE.md` / rules | `GEMINI.md` |
| User-invoked task | Prompt file (`.prompt.md`) | Slash commands | Slash commands, skills | Commands / skills | Custom commands |
| Capability bundle | Skill (`SKILL.md`) | Skill | Skill | Skill | Skill |
| Persona / role | Custom agent (`.agent.md`) | Custom agent | Multi-agent | Subagent | Subagent |
| Lifecycle automation | Hook (`.github/hooks/`) | Hook | Permissions/rules | Hooks | Hooks |
| External tools/data | MCP (`.vscode/mcp.json`) | MCP | MCP | MCP | MCP |
| Packaging | Plugin (`plugin.json`) | Plugin | Config bundles | Plugin | Extension |

## Portability Assessment

### Strong Portability Candidates

These translate well across ecosystems:

- **`SKILL.md`-based skills** — open standard (agentskills.io)
- **`AGENTS.md` guidance** — read by multiple agents
- **MCP concepts** — open protocol, universal transport
- **High-level prompt/instruction patterns** — similar across vendors
- **Directory layout ideas** — skills/, agents/, etc.

### Weak Portability Candidates

These differ significantly between vendors:

- **Hook formats** — each vendor has different event models
- **Agent schemas** — frontmatter fields vary (tools, handoffs, etc.)
- **Plugin manifests** — vendor-specific packaging
- **Command syntaxes** — slash commands differ
- **Subagent semantics** — fork/isolation differs

## Cross-Vendor Adaptation Patterns

When a feature exists in another vendor but not in VS Code, recommend the closest equivalent:

| Other Vendor Feature | VS Code Equivalent |
| --- | --- |
| Claude `context: fork` (isolated execution) | Custom agent with restricted tools |
| Claude `allowed-tools` on skills | Custom agent wrapping the skill with `tools` restriction |
| Gemini TOML custom commands | VS Code prompt files (`.prompt.md`) |
| Gemini read-only plan mode | Planner agent with read-only tools |
| Codex sub-agent exploration | VS Code custom agent + Explore subagent |
| Gemini/Claude rich hook types | VS Code command hooks (simpler model) |

## Generating Cross-Vendor Exports

When generating in `cross-vendor-export` mode:

### 1. Generate the VS Code Target First

Always produce valid VS Code files as the primary output.

### 2. Generate Companion Files

Create vendor-specific files alongside (NOT instead of) the VS Code files:

```text
AGENTS.md                           ← Primary + portable
.github/copilot-instructions.md    ← Optional VS Code compatibility shim
CLAUDE.md                           ← Claude Code compatibility
```

### 3. Mark VS Code-Only Features

When a feature is VS Code-specific, note it:

```markdown
<!-- VS Code only: handoff buttons -->
handoffs:
  - label: Implement Plan
    agent: agent
    prompt: Implement the approved plan above.
```

### 4. Policy for Unsupported Features

If a requested feature exists in another vendor but not VS Code:

1. **Say so** — be explicit about the limitation.
2. **Recommend the closest VS Code equivalent**.
3. **Optionally generate** the vendor-specific export in a separate file.

## Portable Guidance Files

| File | Read By | Purpose |
| --- | --- | --- |
| `AGENTS.md` | VS Code, Codex, Copilot CLI | Universal repo guidance |
| `CLAUDE.md` | VS Code, Claude Code | Claude-compatible guidance |
| `GEMINI.md` | Gemini CLI | Gemini-specific guidance |
| `CODEX.md` | Codex | Codex-specific guidance |
| `copilot-instructions.md` | VS Code | Optional VS Code-specific compatibility guidance |

**Note**: VS Code reads both `AGENTS.md` and `CLAUDE.md` natively. Other vendor files are not read by VS Code.

## Generation Checklist

- [ ] Default mode is `vscode-strict` unless user requests otherwise
- [ ] VS Code files are always the primary output
- [ ] Cross-vendor exports are companion files, not replacements
- [ ] Vendor-specific features not ported across boundaries
- [ ] Portability notes included for each generated artifact
- [ ] Unsupported features documented with closest equivalent
