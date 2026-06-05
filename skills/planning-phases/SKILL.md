---
name: planning-phases
description: >-
  Produce brief, phased implementation plans in markdown with inline progress
  tags, sized for reliable delivery across sessions. Use when the user asks for
  a plan, roadmap, implementation strategy, or multi-step refactor design.
---

# Cursor Skill: Planning Phases

## Intent

When asked to plan work, produce a **numbered implementation plan** in
markdown that is reliable to execute and can be split across consecutive
sessions without losing LLM context.

The plan is the single source of truth. Keep the narrative terse.

---

## Audience and Voice

Unless the user says otherwise:

- **Assume a skilled audience** — prior knowledge of the stack, repo, and
  common engineering trade-offs.
- **Be brief** — no preamble, no recap of what the user already said, no
  motivational filler.
- **Do not elaborate** unless asked — state what will happen, not essays about
  why each line matters.
- **One source of truth** — say each fact once in the plan; do not restate it
  in prose elsewhere.

---

## Phase Structure

Multi-step work must use **numbered phases**. Each phase should be:

- small enough to finish in one focused session when possible
- ordered so later phases depend safely on earlier ones
- named so progress is obvious at a glance

Put phases in the planning markdown document itself — not only in chat.

### Progress tagging

Track completion **inline** on each phase heading or description. Do not add
a separate verbose "progress report" section.

Use a short tag when done; leave untagged when not done.

Good:

```markdown
## 1. Extract validation into `pkg/validate` — DONE

## 2. Wire handlers to the new validator

## 3. Delete orphaned validator code — DONE
```

Also acceptable:

```markdown
1. Extract validation into `pkg/validate` — DONE
2. Wire handlers to the new validator
3. Delete orphaned validator code
```

Bad:

```markdown
## Progress

- Phase 1: complete
- Phase 2: in progress
- Phase 3: not started
```

When a phase completes during implementation, update the tag in the plan
document.

---

## Planning Trade-offs

When choosing how to implement, prefer:

| Prefer | Over |
| --- | --- |
| Code that looks like it had always been written that way | Minimum diff / surgical patch aesthetics |
| Clean end-state shape | Preserving external backward compatibility (unless the user says otherwise) |
| Removing orphans recursively | Leaving dead code, unused exports, stale config, or abandoned paths "for later" |

Do **not** include in the plan:

- narrative about why the change is happening
- history of what the code used to look like
- migration commentary aimed at external consumers (unless the user asks)

Unless the user says otherwise or a later phase depends on it, **remove
anything orphaned by a change — recursively** (unused symbols, files, imports,
config entries, tests for deleted behaviour).

---

## Plan Document Shape

Default markdown outline:

```markdown
# [Task title]

## Goal
[One or two sentences]

## Phases

### 1. [Phase name]
[What changes; key files or packages if known]

### 2. [Phase name]
...

## Out of scope
[Only if needed — brief bullets]
```

Adjust sections only when the user asks for a different shape. Keep optional
sections out unless they add information not already in the phases.

---

## Session Splitting

Size phases so each can be handed to a fresh session with minimal re-discovery:

- name concrete artefacts (packages, types, routes, files) where known
- front-load discovery if the repo is unfamiliar; keep later phases
  mechanical
- avoid phases that mix unrelated concerns
- end each phase in a repo state that builds and tests cleanly when feasible

---

## Rejection Rules

Do NOT produce plans that:

- are long-form narrative when a phased list would suffice
- explain basics to a novice audience without being asked
- duplicate the same decision in multiple sections
- use a dedicated progress appendix instead of inline tags
- optimise for smallest change at the expense of coherent end-state code
- retain orphaned code "just in case" without user instruction
- discuss external backward compatibility unless the user raised it

---

## Operative Rule

Planning output is a **brief, numbered, markdown plan** with **inline DONE
tags**, written for a **skilled reader**, describing an **end-state-shaped**
implementation that **cleans up orphans** — split so it can be executed
 reliably across sessions.
