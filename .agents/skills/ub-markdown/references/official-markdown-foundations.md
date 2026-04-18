# Official Markdown Foundations

Use this reference when Markdown syntax or lint behavior needs grounding in
current official sources instead of habit.

## Primary Sources

### CommonMark

Current official baseline:

- Use the current CommonMark spec as the baseline Markdown syntax reference.
- Source: <https://spec.commonmark.org/>

Use CommonMark for baseline parsing expectations around:

- headings
- paragraphs and blank lines
- lists and list items
- fenced code blocks
- inline code, emphasis, and links

### GitHub Flavored Markdown

Official GitHub dialect reference:

- Use the current GitHub Flavored Markdown spec when GitHub-rendered behavior
  matters.
- Source: <https://github.github.com/gfm/>

Use GFM when repo content depends on GitHub-rendered behavior such as:

- tables
- task lists
- autolinks
- GitHub-specific rendering expectations

### markdownlint

Official rule and inline-configuration behavior:

- Source: <https://github.com/DavidAnson/markdownlint>

Important current points:

1. `markdownlint` honors CommonMark and also supports GFM syntax through its
   parser stack.
2. all rules are enabled by default unless config changes them
3. inline HTML comments can disable, enable, capture, restore, or configure
   rules within a file
4. inline exceptions should stay narrow and justified rather than being used as
   a blanket escape hatch

### markdownlint-cli2

Official CLI behavior:

- Source: <https://github.com/DavidAnson/markdownlint-cli2>

Important current points:

1. `markdownlint-cli2` is configuration-based
2. it is designed to work well with `vscode-markdownlint`
3. quoted globs are recommended for cross-platform compatibility
4. `.markdownlint.jsonc` is one of the supported root configuration formats

### VS Code markdownlint Extension

Official editor behavior:

- Source: <https://github.com/DavidAnson/vscode-markdownlint>

Important current points:

1. default behavior enables all rules except `MD013`
2. project config can come from `.markdownlint.*` or `.markdownlint-cli2.*`
3. the extension respects per-project configuration precedence
4. workspace linting and on-save fixing can be aligned with repo config

## Interpretation For This Repo

Use these sources in this order:

1. repo-local `.markdownlint.jsonc`
2. repo-local lint targets and ignores
3. CommonMark/GFM syntax truth
4. markdownlint rule behavior
5. VS Code extension behavior

That ordering matters.

The repo's lint config is the implementation standard.
The official Markdown specs explain syntax semantics.
The linter docs explain what will be reported and how exceptions work.

## Exception Guidance

If a Markdown lint exception is truly needed:

1. prefer the narrowest inline exception possible
2. disable only the specific rule(s) needed
3. restore the previous state when the exception span ends
4. explain the reason when the exception would not be obvious to a later
   reader

Do not use file-wide disables when a local correction or narrow exception is
possible.
