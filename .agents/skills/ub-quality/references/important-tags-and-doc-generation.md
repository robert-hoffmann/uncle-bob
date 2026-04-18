# Important

These principles apply to **ALL** programming languages and file types.

- **DO NOT REMOVE** relevant comment tags like: BUG, HACK, FIXME, TODO, INFO, IMPORTANT, WARNING
- These are tags added by developers to indicate specific issues or important notes in the code.
- There is a special tag `AGENT_TODO`, that when seen in then comments of code, indicates things that the agent should do, or deeply take into account.
- This explains what changes the agent should make to the code, or what it should take into account when generating new code.
- Once new code is generated, the agent should replace `AGENT_TODO` with `AGENT_DONE` and add a comment that explains what it did, and why it did it.
  - **Unless** the code is something like a JSON file where any type of tag or comment would actually break the file.

## Document generation

- **Do not** create summary documents, manuals, or FAQs, unless the user specifically requests such a file.
- **Do** ask the user whether they want such a document when the changes are
  significant enough that a durable summary would reduce reconstruction cost
  for future maintainers, reviewers, or tool-assisted agents.
