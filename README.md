# cursorlib

Cursor Agent skills: Markdown packs under `skills/<topic>/SKILL.md`. Go, TypeScript/JavaScript, tests, refactors, cross-cutting workflows. Copy into Cursor Agent Skills (e.g. `~/.cursor/skills/` or project-local path; confirm in current Cursor docs).

## Repo shape

- One skill per directory; folder path is the stable git handle.
- Optional YAML frontmatter: `name`, `description`. `description` is the discovery hook when present; some older files use a title instead.
- No build or publish step.

## Install

1. Browse [`skills/`](skills/) and select folders.
2. Copy into your Agent Skills directory.
3. On conflicting instructions, prefer the narrower or task-specific skill; edit local copies as needed.

## Composing skills

- **Tests** — [`test-writing`](skills/test-writing/SKILL.md) assumes [`test-rigour`](skills/test-rigour/SKILL.md), [`test-isolation`](skills/test-isolation/SKILL.md), [`test-fakes-over-mocks`](skills/test-fakes-over-mocks/SKILL.md); add [`test-uniformity`](skills/test-uniformity/SKILL.md) for style.
- **Go application shape** — [`http-handler-dependency-injection`](skills/http-handler-dependency-injection/SKILL.md) with [`go-coding`](skills/go-coding/SKILL.md) and [`refactoring`](skills/refactoring/SKILL.md) when restructuring handlers.
- **Hygiene** — [`dedupe-preemptive`](skills/dedupe-preemptive/SKILL.md) before new helpers; [`documentation-skim`](skills/documentation-skim/SKILL.md) for skim-oriented comments.
- **Planning** — [`planning-phases`](skills/planning-phases/SKILL.md) for phased plans with inline progress tags.
- **Task control flow** — [`procedural-task-entry-points`](skills/procedural-task-entry-points/SKILL.md) when a linear user journey would otherwise become a continuation-registration gate.

## Skill index

- [`dedupe-preemptive`](skills/dedupe-preemptive/SKILL.md) — Reuse existing constructs by semantic role before new helpers, fakes, fixtures.
- [`documentation-skim`](skills/documentation-skim/SKILL.md) — Comments and file-level orientation for skim-reading.
- [`go-coding`](skills/go-coding/SKILL.md) — Mandatory Go edit rules (e.g. no `init()` for package setup).
- [`go-linting`](skills/go-linting/SKILL.md) — Run `golangci-lint` and fix reported issues when requested.
- [`http-handler-dependency-injection`](skills/http-handler-dependency-injection/SKILL.md) — Handlers as composition roots; logic on `Application` with explicit `Dependencies`.
- [`planning-phases`](skills/planning-phases/SKILL.md) — Brief phased plans in markdown with inline DONE tags.
- [`procedural-task-entry-points`](skills/procedural-task-entry-points/SKILL.md) — Task owns the story; reject offer/proceed continuation bags for linear gates (exception: DRY wrapping orchestrators).
- [`refactoring`](skills/refactoring/SKILL.md) — Strengthen separation of concerns without behavior change.
- [`semantic-rename-auditor-for-go`](skills/semantic-rename-auditor-for-go/SKILL.md) — Correct misleading names in small batches; semantics only.
- [`shorten-names-js`](skills/shorten-names-js/SKILL.md) — Shorten overlong JS/TS names while preserving meaning.
- [`skill-firing-diagnostics`](skills/skill-firing-diagnostics/SKILL.md) — Meta: report loaded skills and their effect on the work.
- [`test-fakes-over-mocks`](skills/test-fakes-over-mocks/SKILL.md) — Prefer dedicated fakes over mock libraries.
- [`test-isolation`](skills/test-isolation/SKILL.md) — Independent, deterministic, parallel-safe tests.
- [`test-rigour`](skills/test-rigour/SKILL.md) — Given/When/Then; fixtures as single source of truth; derived expectations.
- [`test-uniformity`](skills/test-uniformity/SKILL.md) — Shared test conventions and common pitfalls.
- [`test-writing`](skills/test-writing/SKILL.md) — Test authoring guided by rigour and isolation.
- [`typescript-coding`](skills/typescript-coding/SKILL.md) — Honest required inputs; explicit data flow; no optional parameters to dodge call-site updates.

YAML `name` may differ from folder name; both refer to the same skill on disk.

## Contributing

Tighter rules, clearer `description` fields, or new skills in the same format. Small reviewable changes matching existing skill tone.
