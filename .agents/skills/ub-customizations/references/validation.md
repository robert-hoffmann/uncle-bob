# Validation Reference

## Output Contract

Every generation response should follow this structure:

1. **Recommendation** — what to generate and why
2. **Assumptions** — defaults chosen, unresolved ambiguities
3. **File tree** — directories and files to create or update
4. **Generated content** — file-by-file output
5. **Validation checklist** — from the relevant section below
6. **Smoke-test prompts** — from the relevant section below
7. **Portability notes** — VS Code-only, Copilot-compatible, or Agent-Skills-portable
8. **Risks / follow-up** — preview features, secrets, trust

## Per-Artifact Validation Checklists

### Skills

- [ ] Directory at `.agents/skills/<name>/` or `.github/skills/<name>/`
- [ ] SKILL.md has `name` and `description` in frontmatter
- [ ] Description is trigger-optimized (what + when + keywords)
- [ ] SKILL.md body under 500 lines
- [ ] References one level deep and linked from SKILL.md
- [ ] Naming: lowercase, hyphens, verb-led, < 64 chars
- [ ] No auxiliary docs (README, CHANGELOG)
- [ ] Scripts tested if included
- [ ] No hardcoded secrets

### Hooks

- [ ] File in `.github/hooks/` directory
- [ ] Correct event type for the use case
- [ ] `type: "command"` specified
- [ ] Command is small and reviewable
- [ ] Conservative timeout set
- [ ] `toolNames` filter when tool-specific
- [ ] Helper scripts executable and tested
- [ ] No hardcoded secrets in commands
- [ ] Preview features noted

### MCP Configs

- [ ] File at `.vscode/mcp.json`
- [ ] Correct transport: `stdio` or `http`
- [ ] Secrets via `inputs` with `password: true`
- [ ] `${input:id}` references correct
- [ ] Descriptive camelCase server name
- [ ] Sandbox considered for untrusted servers
- [ ] Install/test instructions provided

## Smoke-Test Prompts

Generate these test prompts for each artifact type. The user runs them to verify the artifact works.

### For Skills — Trigger Evaluation

Generate 8-10 prompts that **should trigger** the skill:

```text
1. "[Direct request using the skill's primary function]"
2. "[Indirect phrasing that should still activate it]"
3. "[Adjacent terminology the user might use]"
4. "[Specific sub-feature request]"
5. "[Request using different vocabulary]"
6. "[Complex multi-step request within scope]"
7. "[Request combining the skill with another need]"
8. "[Edge case at the boundary of scope]"
```

Generate 8-10 prompts that should **NOT trigger** the skill:

```text
1. "[Simple task handled by built-in tools]"
2. "[Related but out-of-scope request]"
3. "[Request for a different artifact type]"
4. "[Vague request that could match many skills]"
5. "[Request that looks similar but is actually different]"
```

Generate 1-2 boundary cases:

```text
1. "[Request that is too simple — should stay with built-in tools]"
2. "[Adjacent use case that tests scope boundaries]"
```

### For Hooks

For each hook, provide:

- **Event simulation**: How to trigger the lifecycle event
- **Expected behavior**: What should happen (command output, blocked action, etc.)
- **Failure mode**: What happens if the hook script fails
- **Safe case**: One scenario where the hook allows the action
- **Blocked case**: One scenario where the hook blocks or modifies the action

### For MCP Configs

- **Install test**: Steps to install/start the MCP server
- **Auth test**: Verify secret input prompting works
- **Happy path**: One tool call that should succeed
- **Permission note**: What the server can and cannot access

## Human Review Checklist

Every generated artifact should be reviewed by a human for:

- [ ] **Right primitive** — is this the correct artifact type for the need?
- [ ] **Correct paths** — files in the right directories?
- [ ] **Correct names** — following naming conventions?
- [ ] **Valid frontmatter** — all required fields present and correct?
- [ ] **Concise description** — optimized for triggering, not marketing?
- [ ] **Clear "when to use"** — explicit scope boundaries?
- [ ] **Safe defaults** — least privilege, no secrets, review warnings?
- [ ] **No secret leakage** — no hardcoded tokens, keys, or passwords?
- [ ] **No context dump** — lean files, heavy detail in references?
- [ ] **Portability noted** — VS Code-only vs portable features marked?
