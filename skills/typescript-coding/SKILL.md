---
name: honest-typescript-refactoring
description: "Use when composing or modifying TypeScript or JavaScript application code. Enforce honest inputs and explicit data flow."
---

# Honest TypeScript Refactoring

When changing existing code, prefer correctness and clarity over minimising changes.

Treat this as application code, not a public API. Backwards compatibility is not a goal.

## Required

- If a function needs new data, make it a required parameter
- Update all call sites to pass the correct value
- Keep signatures semantically honest
- Make data flow explicit and traceable

## Forbidden

- Do not add optional parameters (`?`) just to avoid updating callers
- Do not add fallback or default logic to compensate for missing inputs
- Do not preserve behaviour by introducing hidden defaults
- Do not add abstraction or wrappers purely to reduce blast radius

## Rule

Missing data must be required and propagated, not absorbed.
