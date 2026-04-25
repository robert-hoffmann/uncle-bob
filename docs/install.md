# Install Uncle Bob

The easiest install path is the open skills CLI. It can install the skill pack
from GitHub into supported agents and can target specific skills or agents when
you do not want the full catalog.

## Recommended: skills.sh

Install the repository:

```sh
npx skills add robert-hoffmann/uncle-bob
```

List available skills before installing:

```sh
npx skills add robert-hoffmann/uncle-bob --list
```

Install selected skills for selected agents:

```sh
npx skills add robert-hoffmann/uncle-bob --skill ub-workflow --agent claude-code codex
```

## Other Install Paths

Copilot users can install from the repository plugin metadata:

```sh
copilot plugin install robert-hoffmann/uncle-bob
```

Teams that need strict review or pinning can vendor the portable skill folders
manually. In that model, copy the skill directories you want and keep updates
under normal code review.

## After Installation

Ask the agent for work in normal language. The skill descriptions are routing
metadata: they tell the agent when a skill should activate.

Examples:

- “Use `ub-workflow` to turn this PRD into a roadmap.”
- “Use `ub-governance` to decide whether this change needs ADR evidence.”
- “Use `ub-ts` to modernize this TypeScript config.”
- “Use `ub-quality` to review this plan for tradeoffs and missing tests.”

## Tradeoffs

`skills.sh`
- Strength: quick install, updates, agent targeting, and skill selection.
- Weakness: teams still need review discipline before broad updates.

Copilot plugin install
- Strength: native path for Copilot users.
- Weakness: less universal across non-Copilot agents.

Manual vendoring
- Strength: maximum control and pinning.
- Weakness: updates are manual and can drift.
