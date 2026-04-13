# cursorlib

**Cursor Agent skills**—versionable instruction packs for coding agents—covering Go, TypeScript/JavaScript, tests, refactors, and a few cross-cutting workflows. Use them as-is, fork them, or steal the ideas for your own rules.

---

## At a glance

| | |
| --- | --- |
| **What** | Markdown skills under `skills/<topic>/SKILL.md`, each with optional YAML frontmatter (`name`, `description`) for discovery. |
| **Why** | Encode recurring engineering judgment once so the agent stays consistent across tasks and sessions—not only in long chat threads. |
| **Scope** | Opinionated defaults (e.g. handler wiring, test rigour, honest TS signatures). Pick what matches your stack; ignore the rest. |

---

## Quickstart

1. **Choose skills** — Browse [`skills/`](skills/); each folder is one skill. The agent usually matches on the skill `description` in frontmatter (where present); some older files lead with a title instead—content still applies.

2. **Install in Cursor** — Copy the folders you want into the directory Cursor uses for **Agent Skills** on your machine (e.g. user-level skills under `~/.cursor/skills/`, or project-local skills if your team uses them). Paths and UI change between releases—check Cursor’s current docs for Agent Skills.

3. **Compose deliberately** — Several skills are meant to work together (see below). If instructions conflict, the narrower or task-specific skill should win; adjust your local copies if needed.

4. **Iterate** — Treat skills like internal coding standards: shorten, split, or tighten when you see the model drift in practice.

---

## The longer story

### Why a library of skills?

Ad-hoc prompts work for one-offs. They do not scale when you care about **stable invariants**—where HTTP logic lives, how tests derive expectations, when to reuse an existing helper vs invent another. Skills are a lightweight way to persist those invariants and load them when the task matches.

### How this repo is organized

- **One skill per directory** — Path name is the stable handle in git; the YAML `name` field may differ (historical or semantic naming).
- **Frontmatter** — When present, `description` is the primary hook for “when should this skill apply?”
- **No runtime** — There is nothing to build or publish. Copy and edit.

### Bundles that compose well

- **Tests** — [`test-writing`](skills/test-writing/SKILL.md) assumes [`test-rigour`](skills/test-rigour/SKILL.md) and [`test-isolation`](skills/test-isolation/SKILL.md); add [`test-uniformity`](skills/test-uniformity/SKILL.md) for style and common pitfalls.
- **Go application shape** — [`http-handler-dependency-injection`](skills/http-handler-dependency-injection/SKILL.md) pairs with [`go-coding`](skills/go-coding/SKILL.md) and [`refactoring`](skills/refactoring/SKILL.md) when you are moving code to match that structure.
- **Hygiene** — [`dedupe-preemptive`](skills/dedupe-preemptive/SKILL.md) before adding helpers; [`documentation-skim`](skills/documentation-skim/SKILL.md) when you want comments optimized for readers skimming large codebases.

### Skill index

| Directory | Summary |
| --- | --- |
| [`dedupe-preemptive`](skills/dedupe-preemptive/SKILL.md) | Reuse existing constructs by **semantic role** before introducing new helpers, fakes, fixtures, etc. |
| [`documentation-skim`](skills/documentation-skim/SKILL.md) | Comments and file-level orientation for skim-reading (TS, JS, Go, Svelte, …). |
| [`go-coding`](skills/go-coding/SKILL.md) | Mandatory rules for Go edits (e.g. `init()` usage). |
| [`go-linting`](skills/go-linting/SKILL.md) | Run `golangci-lint` and fix reported issues when explicitly requested. |
| [`http-handler-dependency-injection`](skills/http-handler-dependency-injection/SKILL.md) | Go HTTP / serverless / GCF: handlers as composition roots; logic on `Application` with explicit `Dependencies`. |
| [`refactoring`](skills/refactoring/SKILL.md) | Strengthen separation of concerns via structure and naming **without** behavior change; defers to stronger architecture skills. |
| [`semantic-rename-auditor-for-go`](skills/semantic-rename-auditor-for-go/SKILL.md) | Correct misleading names in small batches; tests stay green; semantics only, not drive-by refactors. |
| [`shorten-names-js`](skills/shorten-names-js/SKILL.md) | Shorten overlong JS/TS names (files, dirs, symbols) while preserving meaning. |
| [`skill-firing-diagnostics`](skills/skill-firing-diagnostics/SKILL.md) | Meta: have the agent report which skills it loaded and how they affected the work. |
| [`test-isolation`](skills/test-isolation/SKILL.md) | Keep tests independent and robust. |
| [`test-rigour`](skills/test-rigour/SKILL.md) | Rigorous tests: Given/When/Then, fixtures as single source of truth, derived expectations. |
| [`test-uniformity`](skills/test-uniformity/SKILL.md) | Conventions that improve readability and avoid common test mistakes. |
| [`test-writing`](skills/test-writing/SKILL.md) | Practical test authoring guided by rigour + isolation. |
| [`typescript-coding`](skills/typescript-coding/SKILL.md) | TS/JS: honest required inputs, explicit data flow—no optional parameters or hidden defaults to dodge call-site updates. |

YAML `name` values (e.g. `honest-typescript-refactoring`, `separation-of-concerns-refactoring`) may differ from the folder name; both refer to the same skill on disk.

---

## Contributing

Improvements welcome: tighter rules, clearer `description` fields, or new skills in the same format. Prefer small, reviewable changes that match the tone of the existing skills.
