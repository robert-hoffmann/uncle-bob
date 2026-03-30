# Code Formatting & Alignment

These principles apply to **ALL** programming languages and file types.

When an edited block is eligible for alignment under this document, these rules apply.

## The Universal Alignment Rule

> **When you have a vertical list of related items with a separator, align the separators into a column.**

This applies to ALL languages, ALL contexts—code, comments, docstrings, configs, everything.

For eligible vertical separator blocks, separator-column alignment is required. Value-column alignment is non-compliant.

## Alignment Policy Precedence (Agent Contract)

When rules appear to conflict, apply this precedence order:

1. **Syntax Safety First**                  — Never break language syntax or semantic meaning to force alignment
2. **Universal Alignment Rule**             — Align eligible vertical blocks by default
3. **Readability and Padding Guardrails**   — Do not over-pad beyond reasonable thresholds
4. **Local File Conventions**               — Preserve nearby conventions when they do not conflict with the above
5. **Minimal-Diff Discipline**              — Prefer aligning touched blocks; only expand scope when needed for consistency

### Tie-breaker Rules

- If "respect existing formatting" conflicts with the universal rule, align the touched block and leave unrelated blocks unchanged.
- If separator-column and value-column alignment conflict, prefer separator-column alignment (`key : value`) for vertical separator blocks.
- If alignment would require extreme spacing, keep compact formatting and state that a guardrail blocked alignment.
- If tooling rewrites spacing, preserve semantic structure first, then re-apply alignment where possible.

## Eligibility and Decision Framework

Apply alignment rules by separator role, not by programming language.

A touched block is eligible for alignment only when all of the following are true:

1. **Detect a vertical block** — At least 2 adjacent lines with the same separator role (`:`, `=`, `=>`, `->`, `|`, attribute `=`, etc.)
2. **Validate related intent** — Lines represent one logical group (config map, declaration list, params, imports, properties)
3. **Compute target column**   — Separator column is based on the longest left-hand token in the group
4. **Apply guardrails**        — Avoid alignment if it exceeds readability thresholds
5. **Verify scanability**      — Values/comments should form a clean second visual column

### Alignment Guardrails

- **Minimum block size**       : 2 lines
- **Maximum padding per line** : 20 spaces
- **Soft line length target**  : 100-120 characters (language dependent)
- **Hard stop**                : If alignment causes wrapping/churn, prefer compact formatting
- **Scope**                    : Align the edited group first; align neighboring groups only when tightly coupled

Align when:

- Object/dictionary/hash entries
- Variable/constant declaration runs
- Function parameters in multiline signatures
- Interface/type/class field lists
- CSS/SCSS property declarations
- HTML/Vue attribute lists in multiline tags
- Import member lists with trailing comments
- Table-like comment/doc blocks

Do not align when:

- Single-line statements
- Chains/pipelines where spacing obscures flow
- Long expressions where alignment causes heavy wrapping
- Generated/minified files
- Mixed-semantic blocks that only look visually similar

Invalid exceptions:

- Nearby local style
- Convenience or omission
- Preference for a shorter or more familiar value-column style
- The fact that the block is in documentation, comments, or config rather than source code

### The Pattern

```text
<left>   <sep> <right>
<longer> <sep> <right>
<short>  <sep> <right>
```

Where:

- **Left elements**  - are padded with spaces to equal length
- **Separators**     - (`:`, `=`, `->`, `|`, etc.) form a vertical column
- **Right elements** -  start at the same column

### Canonical Colon Alignment Examples

Compliant (separator-column alignment):

```ts
const colors = {
  grid      : '',
  solar     : '',
  textMuted : '',
};

interface ChartColors {
  grid      : string;
  solar     : string;
  textMuted : string;
}
```

```css
:root {
  --color-grid      : oklch(0.55 0.14 260);
  --color-solar     : oklch(0.82 0.17 90);
  --color-textMuted : oklch(0.50 0.02 260);
}
```

Non-compliant for vertical alignment blocks (value-column alignment):

```ts
const colors = {
  grid:      '',
  solar:     '',
  textMuted: '',
};
```

```css
:root {
  --color-grid:      oklch(0.55 0.14 260);
  --color-solar:     oklch(0.82 0.17 90);
  --color-textMuted: oklch(0.50 0.02 260);
}
```

## Multiline Signatures and Attribute Lists

When a callable or declaration has **2+ parameters/attributes** and spans multiple lines, format with one item per line and align separator roles inside that block when the guardrails allow it.

Why:

- Easier to scan related inputs vertically
- Cleaner diffs when adding/removing items
- Consistent with the universal separator alignment rule

## Future Edits Contract

For all future edits, apply these defaults unless the task explicitly says otherwise:

1. Align only touched logical blocks first.
2. Avoid file-wide or repository-wide restyling unless explicitly requested.
3. Preserve syntax/tooling constraints over stylistic preference.
4. Never restyle generated artifacts unless generation requirements changed.
5. Remove transitional labels or migration markers before finalizing code.

## Agent Finalization Gate (Mandatory)

Before finalizing any edit, apply this protocol:

1. **Group**     : Identify alignable vertical blocks in touched regions
2. **Align**     : Apply column alignment using the longest-left-token rule
3. **Constrain** : Enforce padding and line-length guardrails
4. **Verify**    : Re-read for scanability and syntax safety
5. **Exception** : If alignment is not applied, name the guardrail or verified tooling constraint that blocked it
6. **Scope**     : Keep style normalization incremental unless broader migration was requested

## Alignment Quality Checklist

- Separators form a visually straight column
- Right-hand values start at a consistent column
- No line exceeds practical readability due to forced padding
- Unrelated blocks remain untouched (minimal churn)
- Language syntax and runtime semantics are unchanged

## Tooling Interaction Guidance

- If a formatter would erase visual alignment, prefer non-destructive checks over destructive auto-formatting
- If formatter usage is mandatory in a subproject, keep alignment-sensitive blocks scoped and explicit
- During reviews, treat alignment regressions as style defects when they reduce scanability
- In mixed-style files, preserve untouched regions and normalize only edited regions
