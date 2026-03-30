# Base Development Principles

These principles apply to **ALL** programming languages and file types.

Use these principles to guide design decisions whenever tradeoffs arise.

## Design Principles

1. **KISS**  (Keep It Simple, Stupid)   — Favor straightforward solutions over clever ones
2. **DRY**   (Don't Repeat Yourself)    — Extract repeated logic into reusable components
3. **YAGNI** (You Aren't Gonna Need It) — Don't build features until they're actually needed
4. **Single Responsibility**            — Each function, class, or module should do one thing well
5. **Separation of Concerns**           — Organize code so that different concerns (data access, business logic, presentation) are in separate modules or layers

### Guiding Mantra

> **DON'T OVERCOMPLICATE / OVERENGINEER**
>
> Write clean, readable, and maintainable code. If a solution feels complex, step back and simplify.

### Architectural Preferences

- **Prefer composition over inheritance**                — Build behavior by combining small, focused components rather than deep inheritance hierarchies
- **Use third-party packages sparingly and judiciously** — Leverage the language's standard library first; only add dependencies when they provide significant value
- **Comprehensive error handling**                       — Use appropriate error/exception mechanisms with custom error types where beneficial

### Focus Areas (Universal)

These apply regardless of language:

- Performance optimization and profiling
- Memory management awareness
- Type safety (via annotations, hints, or static typing)
- Code readability and maintainability
- Simple, effective solutions
- Async/concurrent programming patterns (where applicable)
- Always use the most modern language features and idioms
- Always apply modern principles like: object-oriented programming, functional programming, modular design, reactive programming, composability, etc. where relevant and beneficial

### Output Expectations

When generating or modifying code:

- Provide clean code with appropriate type annotations/hints
- Include performance benchmarks for critical paths (when relevant)
- Offer refactoring suggestions for existing code
- Include memory/performance profiling results when relevant

### Modern Standards & Best Practices

- Always use the latest standards and industry best practices
- Always be forward thinking: consider how the code will evolve and be maintained in the future
- Always prioritize readability and maintainability

### Evergreen & Forward Compatibility

- **Write for the currently supported version** — Implement against the project's actual supported runtime, framework, and library versions rather than preserving behavior for older versions by default
- **Bias design toward the next upgrade path**  — Structure code so the supported version can move forward cleanly toward newer stable releases and published migration paths
- **Prefer rewrites over compatibility layers** — When modernizing code, replace deprecated patterns with current idioms instead of extending them with shims, fallbacks, bridge code, or legacy wrappers
- **Require explicit justification for backward compatibility** — Add support for older behavior only when a stated runtime contract, supported-platform requirement, staged migration plan, or explicit user requirement makes it necessary

> **Never assume your training data is up to date.**
> Always verify against the latest documentation and resources using the tools at your disposal.
