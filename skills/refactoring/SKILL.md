---
name: separation-of-concerns-refactoring
description: Use when refactoring a Go codebase to assertively strengthen and clarify separation of concerns through package structure, directories, files, and naming, without changing behaviour or overriding stronger architectural skills.
---

## Invariant

Responsibility boundaries should be clear both in the code's behaviour and in the repository structure.

## Rules

- Refactor assertively when the current structure obscures concern boundaries.
- Infer boundaries from responsibilities, dependency direction, cohesion, and reasons for change.
- Preserve externally observable behaviour unless functional change is explicitly requested.
- Use package structure, directories, file splits, moves, extractions, and renames to align the codebase with responsibility boundaries.
- Prefer files that each express a single coherent responsibility.
- Introduce or reshape directories only when they clarify stable concern boundaries.
- Rename files and identifiers when doing so materially improves boundary clarity, navigability, or local consistency.

## Avoid

- speculative abstractions or speculative layering
- gratuitous package or directory nesting
- mechanical file splitting by size alone
- cosmetic renaming without structural benefit
- refactors that weaken or undo stronger applicable skills

## Precedence

This skill is subordinate to stronger architecture and design skills already applicable to the codebase.
