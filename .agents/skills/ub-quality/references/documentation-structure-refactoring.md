# Documentation Requirements

These principles apply to **ALL** programming languages and file types.

Use these requirements to decide what to document, how to organize files, and how to refactor without changing behavior.

## Core Documentation Principles

Good documentation transcends language syntax. These principles apply to **ALL** programming languages.

---

## Function/Method Documentation

Every function, method, or callable should include:

1. **Brief description** — What the function does (one line)
2. **Parameters**        — Each parameter with its type and purpose
3. **Return value**      — What is returned and its type
4. **Exceptions/Errors** — What errors can be raised and when
5. **Example**           — Usage example for non-trivial functions

```text
<doc_block_start>
Brief description of what this function does.

<params_section>
    <param_name>: <type> - Description of the parameter
    <param_name>: <type> - Description of the parameter

<returns_section>
    <type> - Description of what is returned

<errors_section>
    <error_type> - When this error is raised

<example_section>
    <usage_example>
<doc_block_end>
```

**Principle:** A developer should understand how to use a function without reading its implementation.

---

## Class/Type Documentation

Every class, struct, or type definition should include:

1. **Purpose**               — What this type represents
2. **Attributes/Properties** — Key fields and their purposes
3. **Usage context**         — When and how to use this type

---

## Inline Comments

Add inline comments throughout code to explain:

- **Complex logic**        — Algorithms, formulas, or non-obvious operations
- **Business rules**       — Domain-specific requirements or constraints
- **Data transformations** — What data looks like before/after operations
- **Why, not what**        — Explain reasoning, not obvious mechanics

### Comment Quality Standard

- Explain non-obvious logic, business constraints, data shape changes, and trade-offs
- Prefer documenting **why** a decision exists over restating **what** the code already says
- Keep comments close to the logic they clarify
- Remove comments that only narrate obvious operations

---

## Import Statement Documentation

> **Applies to:** All languages with import/include/require statements

Imports are the entry point to understanding a file's dependencies. Document them clearly with inline comments explaining what each import provides.

Use this generic approach:

1. Group dependencies by source (platform/core, external, project-local).
2. Keep one declaration per line for multiline import/include blocks.
3. Add concise role comments for non-obvious dependencies.
4. Align inline role comments inside the same logical block when practical.

**Logical grouping** — organize imports into sections:

1. **Language built-ins / Standard library**
2. **Third-party packages**
3. **Project-specific / Local modules**

Keep section headers and grouping labels language-neutral.

**Principle:** A developer scanning imports should immediately understand what each dependency provides without looking it up.

---

## Variable Naming

- **Use descriptive names**                        — `customerOrderTotal` over `cot` or `x`
- **Comment when purpose isn't immediately clear** — especially for abbreviated names or domain terms
- **Consistent conventions**                       — Follow language idioms (camelCase, snake_case, etc.)

---

## Section Organization

For larger files, use section headers to organize code:

```text
<comment_marker> ============================================================
<comment_marker> Section Name
<comment_marker> ============================================================
```

Or with lighter separators:

```text
<comment_marker> ------------------------------------------------------------
<comment_marker> Subsection Name
<comment_marker> ------------------------------------------------------------
```

**Principle:** A developer scanning the file should quickly understand its structure.

---

## Folding Regions (Where Supported)

Use fold-region markers to improve navigation in larger files where the language/editor supports marker-based folding.

### Enforcement Contract (Hybrid)

- **MUST** use fold regions when a file is `>= 160` lines or has `>= 4` major sections.
- **SHOULD** use fold regions for files between `80-159` lines when scanability is poor.
- **SHOULD NOT** add fold markers to small/simple files (`< 80` lines).

### Region Hygiene Rules

- Use stable Title Case names (for example: `Imports`, `Types`, `Main Logic`).
- Region start/end names must match semantically.
- Maximum nesting depth is 2.
- Do not create empty regions.
- Always close regions before EOF.

### VS Code Canonical Marker Matrix

| File Type | Preferred Marker Pair | Notes |
| --------- | --------------------- | ----- |
| `*.py`, `*.pyi` | `# region Name` / `# endregion Name` | Primary for Python modules and type stubs |
| `*.ts`, `*.js`, `*.mjs` | `// #region Name` / `// #endregion Name` | Primary for script blocks |
| `*.css` | `/* #region Name */` / `/* #endregion Name */` | Keep inside stylesheet logic blocks |
| `*.html` | `<!-- #region Name -->` / `<!-- #endregion Name -->` | For large templates |
| `*.md` | `<!-- #region Name -->` / `<!-- #endregion Name -->` | Useful in long Markdown docs |
| `*.vue` | Marker style by block (`<script>`, `<style>`, `<template>`) | Follow JS/CSS/HTML marker conventions for each block |
| `*.json` | No marker comments | Use structural/object folding only; comments require JSONC |

### Unsupported-Format Fallback

If a language extension does not support region markers:

- Keep visual separator headers (`===`, `---`) for scanability.
- Rely on indentation/syntax-based folding instead of marker comments.

### Reference Links (VS Code)

- Folding basics and marker behavior: <https://code.visualstudio.com/docs/editor/codebasics#_folding>
- Language configuration folding markers: <https://code.visualstudio.com/api/language-extensions/language-configuration-guide#_folding>
- Python language configuration (fold markers): <https://github.com/microsoft/vscode/blob/main/extensions/python/language-configuration.json>
- HTML language support: <https://code.visualstudio.com/docs/languages/html>
- JSON language support: <https://code.visualstudio.com/docs/languages/json>

---

## Documentation Goals

> **Make the code understandable even for developers new to the project.**

Ask yourself:

- Can someone unfamiliar with this codebase understand what this does?
- Are the business rules and constraints documented?
- Is the "why" explained, not just the "what"?

**Principle:** The code IS the documentation — write it so that it tells a clear story.

---

## Code Structure Guidelines

> **Applies to:** All files (`*.*`)

## Core Structure Principles

Well-organized code is easier to navigate, understand, and maintain. These principles apply to **ALL** programming languages.

---

## File Organization

Structure files in a logical, predictable order:

1. **File header/module documentation**
2. **Imports/includes/requires**
3. **Constants and configuration**
4. **Type definitions** (interfaces, types, classes)
5. **Helper/utility functions**
6. **Main logic/exports**
7. **Entry point** (if applicable)

---

## Section Headers

Use visual separators to divide code into logical sections:

### Major Sections (use `===`)

```text
<comment> ============================================================================
<comment> Configuration and Constants
<comment> ============================================================================
```

### Minor Sections (use `---`)

```text
<comment> ----------------------------------------------------------------------------
<comment> Helper Functions
<comment> ----------------------------------------------------------------------------
```

**Principle:** Consistent section markers make scanning large files fast and predictable.

---

## Code Preservation Rules

When modifying existing code:

1. **Preserve all existing functionality** — Don't remove features unless explicitly requested
2. **Keep commented-out sections**         — They often contain important context or fallback code
3. **Maintain existing structure**         — Follow the file's established patterns and organization
4. **Respect existing formatting**         — Match surrounding style unless it conflicts with the alignment policy precedence above
5. **Remove migration-only labels**        — Do not keep transitional markers in final code

---

## Spacing and Readability

1. **Consistent indentation**      — Follow language conventions (spaces vs tabs, indent size)
2. **Blank lines for separation**  — Use blank lines to separate logical blocks
3. **Alignment for related items** — See above: Code Formatting & Alignment
4. **Line length limits**          — Keep lines readable (typically 80-120 characters)

---

## Grouping Related Code

Keep related elements together:

- **Group related functions** — Functions that work together should be near each other
- **Group related imports**   — Organize imports by source (stdlib, third-party, local)
- **Group related constants** — Keep configuration values together

---

## Module/File Size

- **Prefer smaller, focused files** — Each file should have a clear, single purpose
- **Extract when too large**        — If a file grows beyond ~1500 lines (with documentation), consider splitting
- **Balance granularity**           — Don't create files so small they fragment understanding

---

## Refactoring Guidelines

> **Applies to:** All files (`*.*`)

## Core Refactoring Principles

These refactoring practices apply to **ALL** programming languages. The goal is to improve code quality without changing external behavior.

---

## Code Extraction

### Identify Duplicate Code

- Look for repeated patterns across functions or files
- Extract into reusable functions, methods, or utilities
- Use parameters to handle variations

### Break Down Complex Functions

- If a function does multiple things, split it into smaller functions
- Each function should have a single, clear purpose
- Aim for functions that fit on one screen (~20-30 lines)

---

## Naming Improvements

- **Improve variable names** — Rename unclear or abbreviated names to descriptive ones
- **Improve function names** — Names should describe what the function does
- **Consistent naming**      — Follow language conventions throughout the codebase
- **Domain terms**           — Use consistent terminology from the problem domain

---

## Code Cleanup

### Remove Dead Code

- Delete unused variables
- Delete unused functions/methods
- Delete unreachable code branches
- Remove unnecessary comments that state the obvious

### Simplify Logic

- Reduce nesting depth (early returns, guard clauses)
- Simplify boolean expressions
- Replace complex conditionals with named functions
- Use language idioms instead of verbose patterns

---

## Performance Optimization

- **Use efficient algorithms**     — Choose appropriate data structures and algorithms
- **Avoid premature optimization** — Profile first, optimize bottlenecks
- **Memory efficiency**            — Use generators/iterators for large datasets
- **Lazy evaluation**              — Defer computation until needed

---

## Logging and Observability

> **Use logging extensively so we can easily identify errors**

- Add logging at key decision points
- Log function entry/exit for complex operations
- Include relevant context in log messages
- Use appropriate log levels (debug, info, warning, error)

---

## Refactoring Checklist

When reviewing code for refactoring opportunities, check for:

- [ ] Duplicate code that could be extracted
- [ ] Functions doing too many things
- [ ] Unclear or abbreviated names
- [ ] Dead code or unused variables
- [ ] Deep nesting that could be flattened
- [ ] Missing error handling
- [ ] Missing logging for debugging
- [ ] Inefficient algorithms or data structures
- [ ] Magic numbers/strings that should be constants
- [ ] Region markers are balanced in files that use fold regions
- [ ] Region names are meaningful and consistent
- [ ] Region usage is not over-fragmented by excessive nesting/splitting

---

## Safe Refactoring

1. **Make small, incremental changes** — to isolate issues
2. **Verify behavior**                 — after each change
3. **Keep commits focused**            — one refactoring per commit
4. **Preserve fold structure**         — when moving code, preserve or rebalance region boundaries

---
