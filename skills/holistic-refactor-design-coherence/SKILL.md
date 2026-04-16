---
name: holistic-refactor-design-coherence
description: Perform a holistic, multi-session refactor of a JavaScript/TypeScript web app repo to improve design coherence. Only use this skill when explicitly requested by the user. Do not invoke automatically.
---

## Purpose

Review and improve a mature JavaScript or TypeScript web application repository that shows signs of accumulated design drift.

Approach the codebase as a senior engineer would: not by fixing isolated issues, but by identifying the main sources of incoherence and reshaping the system toward a cleaner, more legible, and more maintainable whole.

This is a multi-session activity. Maintain continuity of thought and direction using planning artifacts stored in the repository.

---

## Invocation Rule

- **Do not trigger this skill automatically.**
- **Only use this skill when the user explicitly requests it.**

---

## Assumptions and Scope

- Treat the repository as a web application, not a public library.
- Prefer internal coherence over preserving accidental structure.
- Focus on JavaScript and TypeScript application code.
- Include Python and shell scripts where they affect tooling or workflow.
- Treat technical documentation as part of the design surface where relevant.

---

## What to Look For

Look for patterns, not isolated issues:

- Architectural incoherence
- Structural issues
- Code-level design problems
- Evolutionary drift
- Maintainability friction
- Technical documentation drift

---

## Diagnosis

- Identify a small number of dominant themes.
- Focus on root causes.
- Be concise and opinionated.

---

## Planning and Continuity

Use `/docs/planning/` for:
- planning documents
- state records

At each session:
- read existing docs
- continue work
- update state

---

## How to Act

Work in this order:

1. Clarify boundaries
2. Unify patterns
3. Simplify flows
4. Reorganize structure
5. Improve naming and comments

Prefer simplification over abstraction.

---

## Behavior Preservation

All changes must be semantically lossless:

- Preserve application behavior
- Preserve tooling behavior
- Preserve test intent

- Refactor tests as needed
- Run tests and checks
- Do not introduce behavior changes unless explicitly requested

---

## Goal

Leave the repo:

- coherent
- consistent
- easier to understand
- easier to evolve
