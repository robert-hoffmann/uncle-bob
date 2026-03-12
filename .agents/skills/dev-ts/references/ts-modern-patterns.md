# TypeScript Modern Patterns (Latest Stable)

> Verify these patterns against the latest official TypeScript documentation via web search.

## Goal

Provide portable, modern defaults for the latest stable TypeScript across Node apps, bundler apps, npm libraries, and type-stripping runtimes.

## Archetype Matrix

| Archetype | Runtime authority | Recommended module settings | Emit posture | Notes |
| --------- | ----------------- | --------------------------- | ------------ | ----- |
| Node app | Node runtime | `module: node20` (or `nodenext` when future Node tracking is required) | `tsc` emit or noEmit | Prefer stable Node semantics for production behavior. |
| Bundler app | Bundler resolver and bundler runtime graph | `module: esnext`, `moduleResolution: bundler` | Usually `noEmit: true` | Keep TypeScript focused on typechecking while bundler emits JS. |
| npm library | Consumer runtimes (Node and bundlers) | Prefer `nodenext` or `node20` for compatibility verification | Often declaration-focused emit | Avoid bundler-only assumptions in published packages. |
| Type-stripping runtime | Runtime that erases types only | Modern ESM settings plus `erasableSyntaxOnly: true` | Often `noEmit: true` | Stay inside erasable TypeScript subset. |

## Strict+ Baseline

Use this as the default safety floor unless compatibility requires staged adoption:

- `strict: true`
- `noUncheckedIndexedAccess: true`
- `exactOptionalPropertyTypes: true`
- `verbatimModuleSyntax: true`
- `moduleDetection: force`

Useful additions by context:

- `isolatedModules: true` for mixed transpiler ecosystems.
- `isolatedDeclarations: true` for declaration generation portability.
- `noUncheckedSideEffectImports: true` when side-effect imports exist.
- `rewriteRelativeImportExtensions: true` when emitting JS from TS paths with extensions.

## tsconfig Starting Points

### Node App (LTS)

```jsonc
{
  "compilerOptions": {
    "module": "node20",
    "target": "es2023",
    "lib": ["es2023"],
    "verbatimModuleSyntax": true,
    "moduleDetection": "force",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "types": ["node"],
    "sourceMap": true,
    "skipLibCheck": true
  }
}
```

### Bundler App

```jsonc
{
  "compilerOptions": {
    "target": "esnext",
    "module": "esnext",
    "moduleResolution": "bundler",
    "lib": ["esnext", "dom", "dom.iterable"],
    "verbatimModuleSyntax": true,
    "moduleDetection": "force",
    "isolatedModules": true,
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noEmit": true,
    "types": [],
    "skipLibCheck": true
  }
}
```

### Library Typecheck and Declarations

```jsonc
{
  "compilerOptions": {
    "target": "es2022",
    "module": "nodenext",
    "moduleResolution": "nodenext",
    "lib": ["es2022"],
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "verbatimModuleSyntax": true,
    "moduleDetection": "force",
    "declaration": true,
    "declarationMap": true,
    "emitDeclarationOnly": true,
    "isolatedModules": true,
    "isolatedDeclarations": true,
    "types": []
  },
  "include": ["src"]
}
```

### Type-Stripping Runtime

```jsonc
{
  "compilerOptions": {
    "target": "esnext",
    "module": "esnext",
    "strict": true,
    "erasableSyntaxOnly": true,
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "noEmit": true,
    "skipLibCheck": true
  }
}
```

## Modern Type Patterns

### Validate shape while keeping literals

```ts
type RouteMap = Record<string, { method: "GET" | "POST"; path: `/${string}` }>;

const routes = {
  listUsers: { method: "GET", path: "/users" },
  createUser: { method: "POST", path: "/users" }
} satisfies RouteMap;
```

### Preserve caller literal intent with const type parameters

```ts
function defineStates<const T extends readonly string[]>(states: T): T {
  return states;
}

const states = defineStates(["idle", "loading", "done"]);
```

### Constrain inference edges with NoInfer

```ts
declare function parseWithSchema<T>(schema: T, input: NoInfer<T>): T;
```

### Prefer discriminated unions for stateful logic

```ts
type LoadState =
  | { kind: "idle" }
  | { kind: "loading" }
  | { kind: "success"; data: string }
  | { kind: "error"; reason: string };
```

### Use unknown at trust boundaries

```ts
function parseExternal(input: unknown): { id: string } {
  if (typeof input === "object" && input !== null && "id" in input) {
    const id = (input as { id: unknown }).id;
    if (typeof id === "string") return { id };
  }
  throw new Error("Invalid input");
}
```

## Validation Steps

1. Run project typecheck command.
2. Run lint and tests if available.
3. Confirm module behavior under the real runtime or bundler.
4. Confirm no legacy patterns were introduced.

## Primary Sources

- TypeScript release notes: <https://www.typescriptlang.org/docs/handbook/release-notes/overview.html>
- TSConfig module: <https://www.typescriptlang.org/tsconfig/module.html>
- TSConfig moduleResolution: <https://www.typescriptlang.org/tsconfig/moduleResolution.html>
- TSConfig verbatimModuleSyntax: <https://www.typescriptlang.org/tsconfig/verbatimModuleSyntax.html>
- TSConfig moduleDetection: <https://www.typescriptlang.org/tsconfig/moduleDetection.html>
- TSConfig noUncheckedSideEffectImports: <https://www.typescriptlang.org/tsconfig/noUncheckedSideEffectImports.html>
- TSConfig rewriteRelativeImportExtensions: <https://www.typescriptlang.org/tsconfig/rewriteRelativeImportExtensions.html>
- TSConfig isolatedDeclarations: <https://www.typescriptlang.org/tsconfig/isolatedDeclarations.html>
- TSConfig erasableSyntaxOnly: <https://www.typescriptlang.org/tsconfig/erasableSyntaxOnly.html>
- Node TypeScript docs: <https://nodejs.org/api/typescript.html>
- TypeScript releases: <https://github.com/microsoft/TypeScript/releases>
