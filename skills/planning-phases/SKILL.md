---
name: planning-phases
description: >-
  Produce brief, phased implementation plans in markdown with inline progress
  tags, sized for reliable delivery across sessions. Also covers scripted
  orchestration that runs each phase in a fresh Cursor agent session via a
  fail-fast runner. Use when the user asks for a plan, roadmap, implementation
  strategy, multi-step refactor design, unattended multi-phase execution,
  a phase runner, or one new Cursor session per phase.
---

# Cursor Skill: Planning Phases

## Intent

When asked to plan work, produce a **numbered implementation plan** in
markdown that is reliable to execute and can be split across consecutive
sessions without losing LLM context.

The plan is the single source of truth. Keep the narrative terse.

When the user also wants the work driven unattended across sessions, extend
the same plan with an **execution model** and a **runner** that starts one
fresh Cursor agent per phase. Details are under Scripted multi-session
orchestration below, with a copyable template at
[scripts/run_phases.py](scripts/run_phases.py).

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

When the plan will be script-orchestrated, add an **Execution model** section
and give every implementation phase an **Exit gate** (see below). Prefer a
leading **phase 0** whose only job is to write the runner, unless the user
already has a runner and only wants the remaining phases executed.

---

## Session Splitting

Size phases so each can be handed to a fresh session with minimal re-discovery:

- name concrete artefacts (packages, types, routes, files) where known
- front-load discovery if the repo is unfamiliar; keep later phases
  mechanical
- avoid phases that mix unrelated concerns
- end each phase in a repo state that builds and tests cleanly when feasible

---

## Scripted multi-session orchestration

Use this when the user wants to start a runner and come back to finished
(usually **uncommitted**) work: one **fresh** Cursor agent session per phase,
driven by a script that owns iteration, logging, and fail-fast gating.

This is the captured form of the Cut-command runner precedent: a Python script
shells out to the headless `agent` CLI once per phase, with the plan file as
shared state via inline `— DONE` tags.

### When to add it

Add orchestration to the plan when the user asks for unattended execution, a
phase runner, walk-away completion, or one new Cursor session per phase. Do
not invent a runner for ordinary interactive phase-by-phase work unless they
ask.

### Execution model (in the plan)

State these rules once in the plan, not again in every phase:

- One fresh Cursor agent session per phase — no shared chat context.
- The plan file is the single source of truth; each session receives its phase
  number and reads scope from the plan.
- Sequential and fail-fast: the next session starts only after the current
  phase's exit gate passes.
- No git commits or pushes unless the user explicitly opts in.
- On success, every completed phase heading carries `— DONE`.

### Phase 0 — write the runner

Phase 0 produces the script only. It does not implement the feature.

Copy [scripts/run_phases.py](scripts/run_phases.py) into the repo (typical
home: next to other project scripts), then fill in plan path, workspace,
phase list, and per-phase exit-gate commands. The template already:

1. Preflights that `agent` is on `PATH` and headless auth works.
2. Starts a **new** `agent --print --trust --force` process per phase.
3. Passes a self-contained prompt: plan path, phase number, read-the-plan
   scope, mark `— DONE` on success, do not commit.
4. After each agent returns, checks a completion sentinel in the agent
   output, checks the plan heading is tagged `— DONE`, then runs that
   phase's exit-gate shell command(s).
5. Logs each phase and gate under a tmp log directory; stops on first
   failure.
6. Supports `--start-phase` / `--end-phase` for resume.

**Exit gate for phase 0:** the script exists, is executable, and documents
usage (`--help` or a header). Mark phase 0 `— DONE`, then run the script so
it drives the remaining phases — unless auth or the user blocks that.

Prefer the headless `agent` CLI on `PATH` (as in the template). Use the
Cursor SDK (`Agent.prompt` / `Agent.create`) only when the user asks for it
or the CLI is unavailable; keep the same session-per-phase and fail-fast
contract either way.

### Exit gates

Every implementation phase must declare an **Exit gate** the runner can
execute without trusting the agent's prose alone. Prefer concrete commands
(`make test`, `npm test`, `go test ./...`). Subjective checks (smoke notes,
checklists) need a stable sentinel string in the agent output that the runner
asserts.

### What persists between sessions

The working tree and the plan's `— DONE` tags are the durable state. Runner
logs explain where a fail-fast stop happened. Do not rely on chat history,
and do not commit as a progress mechanism unless the user asked for commits.

### What not to do

- Do not continue the next phase inside the same agent process to "save a
  session". Fresh context is the point.
- Do not put the runner's phase scope essays only in the script when the plan
  already states them — the agent reads the plan; the script names the phase
  and enforces the gate.
- Do not commit, push, or open a PR from the runner unless the plan's
  execution model explicitly allows it.

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
- promise unattended multi-phase execution without a runner, exit gates, and
  the execution-model rules above

---

## Operative Rule

Planning output is a **brief, numbered, markdown plan** with **inline DONE
tags**, written for a **skilled reader**, describing an **end-state-shaped**
implementation that **cleans up orphans** — split so it can be executed
reliably across sessions. When the user wants that execution unattended,
the plan also names the **runner**, **exit gates**, and **no-commit**
(unless opted in) contract, and phase 0 lands a script that starts one
fresh Cursor agent per remaining phase.
