---
name: honest-typescript-refactoring
description: "Use when composing or modifying TypeScript or JavaScript application code. Enforce honest inputs, honest state representation, and explicit data flow."
---

# Honest TypeScript Refactoring

When changing existing code, prefer correctness and clarity over minimising changes.

Treat this as application code, not a public API. Backwards compatibility is not a goal.

## Required

- If a function needs new data, make it a required parameter
- Update all call sites to pass the correct value
- Keep signatures semantically honest
- Make data flow explicit and traceable
- When a field represents a real boolean or present state in application data, represent it explicitly
- Prefer stable, explicit object shapes for current state
- Use optional properties only when absence has a distinct semantic meaning

## Forbidden

- Do not add optional parameters (`?`) just to avoid updating callers
- Do not add fallback or default logic to compensate for missing inputs
- Do not preserve behaviour by introducing hidden defaults
- Do not add abstraction or wrappers purely to reduce blast radius
- Do not omit a boolean field merely to encode the false case
- Do not use optional properties to hide meaningful state
- Do not rely on truthiness or omission when they collapse distinctions that matter to the reader

## Rule

Meaningful state must be represented and propagated explicitly, not hidden in optionality, omission, or defaults.
