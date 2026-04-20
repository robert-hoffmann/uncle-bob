# Prompt & Instruction Engineering Reference

Use this reference to generate prompts, instructions, skills, and agent bodies that trigger reliably, constrain behavior clearly, and avoid vague guidance.

## Canonical Structure for Generated Content

Use this consistent structure when generating prompts, instructions, skills, or agent bodies:

1. **Identity / role** — who or what is this?
2. **Mission / goal** — what is the primary objective?
3. **When to use** — trigger conditions and scope
4. **Constraints / boundaries** — what NOT to do
5. **Procedure / workflow** — step-by-step guidance
6. **Tool guidance** — when and how to use available tools
7. **Output format** — expected structure of results
8. **Validation / definition of done** — acceptance criteria
9. **Examples** — concrete good and bad examples
10. **References** — links to supporting files

Not every section is needed for every artifact. Use the sections that apply.

## Description-Writing Formula for Skills

The shared skill-description routing formula now lives in
[`../../ub-authoring/references/authoring-conventions.md`](../../ub-authoring/references/authoring-conventions.md).

Use that shared reference for reusable description guidance.
Keep this file focused on prompt, instruction, and artifact-structure guidance
that is specific to customization work.

## Instruction-Writing Rules

Generated instructions should:

- Be **concise and actionable** — no filler.
- Focus on **non-obvious rules** the model would not already know.
- Show **desired and avoided patterns** with short code examples.
- Include **examples where ambiguity is likely**.
- Avoid duplicating what **linters/formatters already enforce**.
- Use **imperative** form: "Use X", "Prefer Y".
- Prefer **explicit acceptance boundaries** over soft wording like "when practical" or "best effort" unless a real exception boundary is intended.
- State **defect states or non-compliant patterns** when failure modes are predictable.

### Good Pattern

```markdown
## TypeScript conventions
- Prefer `interface` over `type` for object shapes.
- Use `unknown` instead of `any` at API boundaries.
- Example:
  ```ts
  // Good
  function parse(input: unknown): Result { ... }
  // Avoid
  function parse(input: any): Result { ... }
  ```

```markdown

### Bad Pattern

```markdown
## TypeScript conventions
- Follow TypeScript best practices.
- Write clean code.
- Be sure to handle errors appropriately.
```

## Prompt-Writing Rules

Generated prompts should:

- Specify **inputs, outputs, and constraints** clearly.
- **Break down** complex work into numbered steps.
- Include **acceptance criteria** or expected output format.
- Avoid **vague verbs** like "improve" without defining what improvement means.
- Tell the model **when to ask questions** vs proceed autonomously.
- Prefer **concrete over abstract**: "Check for SQL injection in query builders" over "Review security."
- Prefer **named boundaries and exclusions** over open-ended scope.
- Replace soft requests like "make it better" with concrete criteria, defect classes, or measurable outcomes.

## Tool Guidance Rules

When generating agent or prompt tool configurations:

- Expose **only relevant tools** — least privilege.
- Keep the **active tool set small** — models perform better with fewer tools.
- Document **tool intent** clearly in the agent/prompt body.
- Prefer **tool names and outputs that are high-signal**.
- Avoid returning noisy identifiers that do not help downstream decisions.

## Progress & Planning Patterns

For long-running or complex workflows, generated artifacts should encourage:

1. **Short upfront plan** — state what will be done before doing it.
2. **Progress checkpoints** — update the user at key milestones.
3. **End-state summary** — confirm what was accomplished.
4. **Explicit verification steps** — how to test the result.

## Examples Over Abstract Admonitions

When generating any artifact, include:

- **1-2 good examples** showing the desired behavior or output.
- **Optional anti-examples** when misuse is likely.
- Use concrete, minimal examples — not lengthy tutorials.
- Keep examples close to the rule they clarify so the model does not need to infer the connection.

### Why This Matters

This is the customization-specific extension of the shared authoring rule that
examples beat vague admonitions.

Models follow examples more reliably than abstract instructions:

```markdown
# Good: concrete procedure
## Commit messages
Use conventional commits: `type(scope): description`
- `feat(auth): add OAuth2 provider`
- `fix(api): handle null response body`
- NOT: `updated stuff` or `wip`

# Bad: vague admonition
## Commit messages
Write clear and descriptive commit messages following best practices.
```

## Naming Conventions (All Artifact Types)

Use the shared naming conventions in
[`../../ub-authoring/references/authoring-conventions.md`](../../ub-authoring/references/authoring-conventions.md).

For customization artifacts specifically, namespace by tool when it improves
clarity, for example `gh-address-comments`.
