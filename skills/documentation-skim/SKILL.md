---
name: documentation-skim
description: >-
  Add or refine comments for human skim-reading: high-level orientation without
  redundant restatement of the code—including optional file-level headers that
  place a module on a repo map. Use when documenting TypeScript, JavaScript,
  Go, Svelte, or other languages where the user wants reader-efficient prose.
---

# Documentation for skim readers

## When to apply

- The user asks for comments, docstrings, or API documentation with **reader
  efficiency** in mind.
- The user references **skimming**, **big-picture**, **orientation**, or **not
  commenting every line**.
- The user asks for a **top-of-file** header, **module story**, **where this fits in
  the repo**, or a **rollout** of such headers (e.g. under `src/`, `tools/`,
  excluding tests).

## Purpose (why comment)

Comments are a **fast path** for humans: they let someone **skim** a file, type, or
function and build a **coarse mental model**—what subsystem this is, what data flows
where, which invariants and edge cases matter—**without** reading every line. A good
comment can act as a **proxy for reading the implementation** when the reader only
needs direction, not proof.

High-level comments may be **intentionally slightly vague** when that is enough to
orient a reader; **precision** belongs in names, types, and code. Prefer **one
orienting sentence** over repeating what the next five lines do.

At **file** granularity, the same idea applies: give a **map-level** mental model
(subsystem, typical upstream/downstream direction, owned responsibility)—not a
substitute for reading imports or types when the reader needs proof.

## Style (when you do write)

- Use **identifier-first** phrasing (Go doc style): start with the name of the type,
  function, field, or variable, then one clear sentence on **responsibility** and,
  when useful, **inputs → outputs** or **observable effects** (I/O, storage, globals,
  errors).
- For **file-level** headers, lead with the **module or file name** (as the reader
  sees it), then the orienting sentences below.
- Match the project’s existing comment syntax (`//`, `/* */`, `/** */`, `#`, etc.).

## What to prioritize

1. **Exported / public API** and anything **cross-package** or **cross-boundary**.
2. **Domain rules** and **non-obvious contracts** (e.g. exclusive vs inclusive time
bounds).  3. **Side effects** and **failure modes** (network, disk, auth, caching).
4. **Private helpers** only when behavior or misuse risk is **not obvious** from the
name plus a quick read of the body.  5. For **file-level** headers: **subsystem
boundaries**, **data or control direction** (who typically consumes this, what this
usually feeds), and **owned responsibility**—not an export inventory.

## Mission: file-level orientation (repo context)

Use this when the user wants a **skim header at the top of a source file** (often as
part of a directory rollout). Goal: a cold reader builds a **short story**—what this
module is for **in the codebase**, what it **owns**, and how it **fits** among
neighbors.

### Content contract

Each file-level block should include:

1. **Repo context (about one sentence):** Directional placement—typical **upstream →
this module → downstream** (what calls or drives it, what it feeds). This is a
**map**, not a complete dependency graph.  2. **Owned responsibility:** What this
file or module **owns** versus what it **delegates** elsewhere.  3. **Conceptual
kind:** **One primary** label for the module’s stance (see **Reference: conceptual
kinds** below). The project or user prompt may supply a different list; follow that
when given.  4. **Optional:** One line of **non-goals** (“does not …”) to bound
responsibility for skimmers.

Keep the block **compact** (a few sentences). Do not replace good file names or
folder structure with a wall of text.

### Accuracy and scope drift (explicit boundary)

- Default: headers are **reader-oriented orientation**. The skill **does not**
  require auditing the repo (imports, call sites, docs) to **prove** every clause
  unless the **user’s prompt** asks for that (e.g. validate the header against the
  codebase, list mismatches).
- Do **not** claim exhaustive callers, complete architecture, or guaranteed freshness
  unless the user asked for validation or the evidence is in the immediate task
  context.

### Reference: conceptual kinds (examples)

Pick **one primary** label per file; add a short qualifier if needed. User or project
may override this vocabulary.

- **Definition** — domain meaning: types, schemas, constants, shared vocabulary
- **Pure logic** — deterministic transforms; no I/O
- **Query / selector** — reads or derives state or views from existing data
- **Service** — operations behind a clear contract (stateless or stateful)
- **Orchestrator / coordinator** — wires steps; owns control flow
- **Adapter / boundary** — HTTP, filesystem, DB, third-party SDK, env
- **Pipeline stage** — one step in a multi-file build or data flow
- **UI shell** — composition, routing, wiring (not low-level drawing)
- **Presentation** — rendering, formatting, visual mapping for display

## What to omit (discretion)

- **Do not** add a comment that only **restates the identifier and type signature**
  or the **next two lines of code**.
- **Do not** comment every **local variable** in small functions or inside each
  **`it()`** block in tests.
- If a single **type-level** or **function-level** comment would replace five
  redundant line comments, **merge upward** or **drop** the line comments.
- If unsure: favor **orientation for a skimmer** over **line-by-line narration**.
- For **file-level** headers: **do not** paste **export lists** or use **path /
  package.json repetition** as the only “context.” **Do not** promise exhaustive
  callers unless the user asked for validation.

## Tests

- Document **shared helpers**, **fixtures**, **fakes**, and **non-obvious test data**
  that encode a contract.
- Skip noise on **routine locals** unless they encode a subtle invariant worth a
  one-liner.

## Optional accountability

When the user wants transparency, end with a **short list** (e.g. 2–4 bullets) of
**where you chose not to comment** and **one phrase each** for why (e.g. “name + body
self-explanatory”, “only call site for obvious helper”).

## What not to do

- Do not use comments to **replace** good naming or types.
- Do not expand scope (refactors, renames) unless the user asked; **comments only**
  unless they request otherwise.
