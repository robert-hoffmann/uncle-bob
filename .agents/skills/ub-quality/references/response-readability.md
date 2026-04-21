# Response Readability

Use this reference to keep user-facing responses easy to scan across chat,
planning, reviews, specs, and explanations.

The goal is durable structure, not visual flourish. Prefer patterns that work
cleanly in plain Markdown, narrow chat panes, and weaker renderers.

## Durable Rules

Apply these as the default readability contract:

- Lead with the answer, recommendation, or key point.
- Chunk substantial responses into short sections with useful headings.
- Keep paragraphs short and visually separated.
- Use bullets for collections and numbered steps for sequence.
- Keep list items parallel in grammar and purpose.
- Use tables only when they stay compact and genuinely improve comparison.
- Fall back to stacked option sections when table width hurts scanability.
- Keep short answers compact instead of over-structuring them.

## Scanning And Hierarchy

Use structure to reduce reconstruction cost for the reader.

Prefer:

- answer-first or recommendation-first openings
- summary-first organization for longer responses
- short headings that tell the reader what the next section contains
- one idea cluster per paragraph or list block

Avoid:

- buried conclusions
- long openings that delay the actual answer
- headings like `Notes` or `Details` when a more specific title would help

## Lists And Steps

Use the list shape that matches the content:

- use bullets for unordered collections, options, and grouped observations
- use numbered lists for sequence, procedure, or priority
- use stacked term-list style blocks when each item needs a short label plus a
  few supporting lines

Keep lists readable:

- give the list a short introductory line when context is needed
- keep items parallel in grammar and scope
- prefer concise items over paragraph-length bullets
- split a dense list when the reader would benefit from smaller groups

## Tables And Fallbacks

Tables help when the reader needs true side-by-side comparison across multiple
attributes. They stop helping once width or cell density takes over.

### Use A Table When

- each row has the same small set of attributes
- the comparison is easier side by side than in prose
- headers can stay short
- cells can stay brief
- the table can usually stay within `2-4` columns

### Avoid A Table When

- the content is mostly prose
- a single option needs several lines of explanation
- the table would need long headers to make sense
- the comparison is really a short list of labeled observations
- the host is likely to render Markdown tables poorly

### Default Fallback

When a table stops helping, convert it to stacked option sections or a term
list instead of forcing the grid to survive.

Preferred fallback shape:

```markdown
`Option name`
- Strength: What it does well
- Weakness: What it costs or risks
- Best when: The situation where it fits
```

Use this fallback when:

- headers become long
- any column needs sentence-length explanation
- the table becomes visually dense
- the renderer is likely to handle the table poorly
- the comparison reads more naturally as stacked option sections

Do not rely on hard line breaks or manual wrapping inside Markdown table cells
as the primary fix.

## Readable Prose

Readable prose is usually:

- concrete before abstract
- short before long
- explicit before implied

Prefer:

- direct wording
- visible transitions when the argument changes direction
- one recommendation per section before supporting detail

Avoid:

- large uninterrupted prose blocks
- repeated framing that adds no information
- mixing explanation, comparison, and procedure in the same dense paragraph

## Host-Aware Limits

This skill can control content structure, not final typography.

Treat these as non-policy concerns:

- exact fonts
- serif versus sans choices
- exact spacing scales
- strict character-count thresholds for tables
- renderer-specific wrapping assumptions

Use soft heuristics instead:

- if a table feels wide, dense, or brittle, rewrite it
- if a paragraph feels long enough to hide the point, split it
- if headings or bullets do not improve scanning, remove them

## Examples

### Explanation

Good:

```markdown
## Why It Failed

The request failed because the config loader only checks workspace-local files.
The user path is ignored.

## Fix

Add the user-scope lookup after the workspace lookup and keep workspace values
as the higher-precedence source.
```

Too dense:

```markdown
The request failed because the config loader only checks workspace-local files and ignores the user path, so the fix is to add the user-scope lookup after the workspace lookup while preserving workspace precedence.
```

### Comparison

Good compact table:

```markdown
| Option | Strength | Weakness |
| --- | --- | --- |
| Cache | Fast reads | Invalidation complexity |
| Query | Fresh data | Higher latency |
```

Good fallback:

```markdown
`Cache`
- Strength: Fast reads
- Weakness: Invalidation complexity

`Query`
- Strength: Fresh data
- Weakness: Higher latency
```

Too dense:

```markdown
| Option | Strengths and weaknesses in realistic production usage |
| --- | --- |
| Cache | Fast reads, but invalidation and consistency become difficult once the write path and background refresh logic grow beyond a simple single-node deployment. |
```

### Plan

Good:

```markdown
## Summary

Add user-scope config lookup without changing workspace precedence.

## Key Changes

1. Read workspace config first.
2. Read user config second.
3. Merge with workspace taking precedence.
```

Too dense:

```markdown
We should add user-scope config lookup without changing workspace precedence and the implementation should read workspace config first, then user config, and then merge them so workspace still wins.
```

### Review

Good:

```markdown
## Findings

1. The cache key omits locale, so cross-locale collisions are possible.
2. The fallback path skips input validation and can accept malformed values.
```

Too dense:

```markdown
There are two main issues: the cache key omits locale which can cause collisions, and the fallback path skips validation and can therefore accept malformed values.
```

### Procedure

Good:

```markdown
1. Open the settings file.
2. Add the new key.
3. Restart the service.
```

Too dense:

```markdown
Open the settings file, add the new key, and restart the service.
```

## Advisory Heuristics

These heuristics can help, but they are not hard policy:

- extremely long lists often read better when split into smaller groups
- wide comparisons often read better as stacked sections
- print and web line-length guidance can inform judgment, but should not become
  strict chat-output rules
- typography research can inform caution about density and legibility, but this
  skill should not pretend to control host typography

## Evidence Appendix

These sources materially shaped the rules above:

- Microsoft Style Guide on scannable content, lists, tables, and responsive
  content
- Google developer documentation guidance on lists and tables
- W3C guidance on readable and understandable text
- selected readability and typography research, including work on legibility,
  print size, and text-rich interface reading

Source links:

- <https://learn.microsoft.com/de-de/style-guide/scannable-content/>
- <https://learn.microsoft.com/fr-fr/style-guide/scannable-content/lists>
- <https://learn.microsoft.com/ja-jp/style-guide/scannable-content/tables>
- <https://learn.microsoft.com/en-us/style-guide/responsive-content>
- <https://developers.google.com/tech-writing/one/lists-and-tables>
- <https://developers.google.com/style/lists>
- <https://developers.google.com/style/tables>
- <https://www.w3.org/WAI/WCAG21/Understanding/readable.html>
- <https://pubmed.ncbi.nlm.nih.gov/31078662/>
- <https://pubmed.ncbi.nlm.nih.gov/21828237/>
- <https://pubmed.ncbi.nlm.nih.gov/16099015/>
- <https://pubmed.ncbi.nlm.nih.gov/25075429/>
