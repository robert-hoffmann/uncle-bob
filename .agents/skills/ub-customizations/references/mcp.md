# MCP Server Configuration Reference

## When to Use MCP

Use MCP when the model needs **tools, resources, or data outside the local workspace**. MCP (Model Context Protocol) bridges Copilot to external systems.

**Good use cases:**

- Issue trackers (Jira, Linear, GitHub)
- Databases (PostgreSQL, MongoDB, BigQuery)
- Cloud APIs (AWS, Azure, GCP)
- Internal APIs and services
- Browser automation (Playwright)
- Remote documentation services (Context7)
- Authentication services

**Do NOT use MCP when:**

- The capability is fully local and simple → use a script
- The model only needs guidance or a reusable local procedure → use a skill or
  other non-MCP customization surface
- A shell command is enough → use a hook or script

## Config File

**Location**: `.vscode/mcp.json` (workspace) or user settings.

## Structure

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "api-token",
      "description": "API token for the service",
      "password": true
    }
  ],
  "servers": {
    "server-name": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@example/mcp-server"],
      "env": {
        "API_TOKEN": "${input:api-token}"
      }
    }
  }
}
```

## Transport Types

### stdio (Local Process)

The server runs as a local child process communicating via stdin/stdout.

```json
{
  "servers": {
    "my-server": {
      "type": "stdio",
      "command": "node",
      "args": ["./path/to/server.js"],
      "env": {
        "SECRET": "${input:my-secret}"
      }
    }
  }
}
```

**Use for**: locally installed servers, development servers, npm packages.

### http (Remote Server)

The server runs remotely, accessed via HTTP with Server-Sent Events (SSE).

```json
{
  "servers": {
    "remote-api": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${input:api-token}"
      }
    }
  }
}
```

**Use for**: remote services, shared team servers, SaaS integrations.

## Input Variables for Secrets

**Never hardcode secrets.** Use the `inputs` array to prompt the user securely:

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "jira-token",
      "description": "Jira API token",
      "password": true
    }
  ],
  "servers": {
    "jira": {
      "type": "http",
      "url": "https://company.atlassian.net/mcp",
      "headers": {
        "Authorization": "Bearer ${input:jira-token}"
      }
    }
  }
}
```

**Reference syntax**: `${input:<id>}` in `env`, `args`, `headers`, or `url` fields.

## Sandbox Support

On macOS and Linux, stdio servers can run in a sandbox for additional security:

```json
{
  "servers": {
    "sandboxed-server": {
      "type": "stdio",
      "command": "node",
      "args": ["./server.js"],
      "sandbox": true
    }
  }
}
```

Use sandboxing for untrusted or third-party MCP servers.

## MCP Capabilities

MCP servers can expose:

| Capability | Description |
| --- | --- |
| **Tools** | Functions the agent can call (query database, create ticket, etc.) |
| **Resources** | Data sources the agent can read (documentation, schemas, configs) |
| **Prompts** | Pre-built prompt templates from the server |

The VS Code output should stay grounded in what VS Code surfaces clearly for end users. Tools are the most common capability.

## Server Naming

- Use **descriptive camelCase** names: `jiraCloud`, `postgresDb`, `playwrightBrowser`.
- Names should indicate what the server connects to.
- Keep names short but clear.

## Template: stdio Server (npm package)

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "db-connection",
      "description": "PostgreSQL connection string",
      "password": true
    }
  ],
  "servers": {
    "postgresDb": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${input:db-connection}"
      }
    }
  }
}
```

## Template: http Server (Remote API)

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "api-key",
      "description": "Service API key",
      "password": true
    }
  ],
  "servers": {
    "remoteService": {
      "type": "http",
      "url": "https://api.example.com/v1/mcp",
      "headers": {
        "Authorization": "Bearer ${input:api-key}"
      }
    }
  }
}
```

## Generation Defaults

- Always use **`inputs` for secrets** — never hardcode tokens, keys, or passwords.
- Use **descriptive camelCase** server names.
- Favor **least privilege** — only expose tools the workflow needs.
- Consider **sandboxing** for local stdio servers from untrusted sources.
- Include **install/test instructions** as comments or companion documentation.
- For development servers, include **watch/debug hints**.

## Generation Checklist

- [ ] File location: `.vscode/mcp.json`
- [ ] Correct transport type: `stdio` for local, `http` for remote
- [ ] Secrets use `inputs` with `password: true` — never hardcoded
- [ ] Descriptive camelCase server name
- [ ] `env` or `headers` reference inputs via `${input:id}` syntax
- [ ] Sandbox considered for untrusted servers
- [ ] Install and test instructions provided
- [ ] No plaintext secrets committed to repo
