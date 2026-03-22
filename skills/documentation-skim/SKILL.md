---
name: documentation-skim
description: >-
  Add or refine comments for human skim-reading: high-level orientation without
  redundant restatement of the code. Use when documenting TypeScript, JavaScript,
  Go, Svelte, or other languages where the user wants reader-efficient prose.
---

# Documentation for skim readers

## When to apply

- The user asks for comments, docstrings, or API documentation with **reader efficiency** in mind.
- The user references **skimming**, **big-picture**, **orientation**, or **not commenting every line**.

## Purpose (why comment)

Comments are a **fast path** for humans: they let someone **skim** a file, type, or function and build a **coarse mental model**—what subsystem this is, what data flows where, which invariants and edge cases matter—**without** reading every line. A good comment can act as a **proxy for reading the implementation** when the reader only needs direction, not proof.

High-level comments may be **intentionally slightly vague** when that is enough to orient a reader; **precision** belongs in names, types, and code. Prefer **one orienting sentence** over repeating what the next five lines do.

## Style (when you do write)

- Use **identifier-first** phrasing (Go doc style): start with the name of the type, function, field, or variable, then one clear sentence on **responsibility** and, when useful, **inputs → outputs** or **observable effects** (I/O, storage, globals, errors).
- Match the project’s existing comment syntax (`//`, `/* */`, `/** */`, `#`, etc.).

## What to prioritize

1. **Exported / public API** and anything **cross-package** or **cross-boundary**.
2. **Domain rules** and **non-obvious contracts** (e.g. exclusive vs inclusive time bounds).
3. **Side effects** and **failure modes** (network, disk, auth, caching).
4. **Private helpers** only when behavior or misuse risk is **not obvious** from the name plus a quick read of the body.

## What to omit (discretion)

- **Do not** add a comment that only **restates the identifier and type signature** or the **next two lines of code**.
- **Do not** comment every **local variable** in small functions or inside each **`it()`** block in tests.
- If a single **type-level** or **function-level** comment would replace five redundant line comments, **merge upward** or **drop** the line comments.
- If unsure: favor **orientation for a skimmer** over **line-by-line narration**.

## Tests

- Document **shared helpers**, **fixtures**, **fakes**, and **non-obvious test data** that encode a contract.
- Skip noise on **routine locals** unless they encode a subtle invariant worth a one-liner.

## Optional accountability

When the user wants transparency, end with a **short list** (e.g. 2–4 bullets) of **where you chose not to comment** and **one phrase each** for why (e.g. “name + body self-explanatory”, “only call site for obvious helper”).

## What not to do

- Do not use comments to **replace** good naming or types.
- Do not expand scope (refactors, renames) unless the user asked; **comments only** unless they request otherwise.
