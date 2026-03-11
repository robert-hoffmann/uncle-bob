---
name: governance-help
description: Interactive entrypoint for governance help. Routes to the governance-help custom agent and keeps answers grounded in the current governance skill.
argument-hint: "overview | evidence | testing | repository | core | glossary | invoke <skill>"
agent: governance-help
---

# Governance Help

Use the `governance-help` custom agent for this request.

Interpret any text after `/governance-help` as the requested help topic.

Behavior:

- No topic: return a concise overview and list the available topics.
- Topic provided: route to the matching governance topic and answer from the current governance skill and the minimum necessary references.
- `invoke <skill>`: explain which governance skill or mode to use and provide a short paste-ready example grounded in the current source files.

Available topics:

- `overview`
- `evidence`
- `testing`
- `repository`
- `core`
- `glossary`
- `combos`
- `invoke <skill>`
