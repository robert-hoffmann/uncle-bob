// TypeScript ESLint starter.
// Use this only when the target repository wants ESLint in addition to the
// TypeScript baseline. Install the required dev dependencies before relying on
// this config in CI or local automation.

import js from "@eslint/js";
import { defineConfig } from "eslint/config";
import tseslint from "typescript-eslint";

export default defineConfig(
  {
    ignores: ["dist/**", "coverage/**", "node_modules/**"],
  },
  js.configs.recommended,
  tseslint.configs.recommended,
);
