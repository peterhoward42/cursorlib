---
name: dedupe-preemptive
description: Prevent accidental semantic duplication during development by reusing existing repository constructs before introducing new ones.
---

# dedupe-preemptive

Prevent accidental duplication during implementation.

This skill performs a **local reuse check** anchored to the construct being introduced.  
It is **not** a repository-wide deduplication or cleanup pass.

**Principle**

Reuse existing repository concepts before inventing new local ones.

## When to apply

Use this skill whenever code introduces a new:

- helper
- abstraction
- fake or stub
- fixture or builder
- validator
- mapper
- utility
- wrapper or adapter
- convenience function
- local pattern

This commonly occurs in:

- tests
- handler wiring
- infrastructure adapters
- support utilities
- request validation
- domain helpers

## Instructions

Before introducing a new construct:

1. Search the repository for an existing construct that already serves the same **role**.
2. Search by **semantic role**, not just by exact name.
3. Prefer reusing existing repository vocabulary and patterns.
4. If an existing construct is close but incomplete, prefer **extending or adapting it**.
5. Only introduce a new construct if existing ones are **materially insufficient**.
6. If a new construct is still introduced, briefly explain why reuse was not appropriate.

## Recognising overlapping roles

Two constructs may represent the same role when they share most of:

- contract
- purpose
- dependency role
- policy encoded
- lifecycle role
- test-support role

Names alone are not reliable indicators.

Example overlaps:

