---
name: code-review-findings
description: >-
  Perform an actual code review of changed DrawExact code for Pete and report a
  short, prioritised set of findings, judged by the criteria he cares about
  most and silent on the areas he is content to risk. Use when Pete asks for a
  code review, review findings, or a reviewer's verdict on changed code. Not
  for a code review guide, which is the ai-code-review skill.
---

# Code review findings

## What this skill is for

Pete usually reviews changes himself, steered by a navigation guide that the `ai-code-review` skill produces. This skill covers the times he asks for the review itself: a reviewer's judgement on a body of changed code, delivered as a small number of findings that each deserve his attention.

The central idea is selectivity. Pete finds exhaustive review output overwhelming, and he is content to accept risk in areas he does not care much about. A review that reports everything it noticed has failed, however accurate each point is. The value of this skill lies in knowing which things matter to him, so most of it describes his sensitivities, and then the areas he does not want to hear about.

## Establish scope and intent first

Pete names the scope. It is usually a phase implemented in the current session, a list of commits, or a feature branch compared with `main`, and it often spans both `dxact-wasm` and `dxact-draw`. Review the named changes as one whole, and ignore unrelated commits that sit between them. If the scope is ambiguous, work out the candidate commits and ask him to confirm before reviewing.

Next, find out what the change was meant to achieve before judging how it achieves it. The intent usually lives in a plan or analysis document under `dxact-wasm/docs`. Also read the architecture documents that bear on the touched packages, starting from `docs/architecture/architecture-orientation.md`, because they record the ownership principles Pete expects the code to obey. The documents under `docs/design` are the contract a future reader will trust, so a change that alters behaviour they describe should have updated them too.

The review is read-only. Do not fix anything while reviewing, even when the fix is obvious, because Pete triages the findings himself and often wants to discuss one before anything changes. Running tests, lint, or a compiler diagnostic to confirm a suspicion is fine.

## What Pete cares about

The concerns below are ordered roughly by how strongly and consistently he has reacted to them in past reviews.

### Names that a newcomer can read

Pete reacts to names more often than to anything else. People other than Pete read this code, including his development partner Perran, so a name has to mean the right thing to a competent developer who lacks Pete's particular background. Raise a name in any of these cases.

- It borrows vocabulary from a specialist field the reader cannot be assumed to know. `bandPass` was rejected because it relies on signal-processing knowledge. Vocabulary native to the subsystem is fine, such as rendering and scene-graph terms inside the renderer.
- It is a metaphor that pulls the mind somewhere else. `Drawer` suggested a chest of drawers and became `Driver`, and `arm` for a developer-only trigger became `fake`. Pete reads "shell" as bash and "chrome" as the browser, so avoid those for UI concepts too.
- It is a word with too many plausible meanings in context, such as `type`, `pass`, or `identity`.
- It hides part of what it tests, or sounds as if it has a side effect. `accepts(key)` became `isOpenFor(key)` because it checks both that the path is open and that the key matches.
- It breaks the symmetry of parallel things. Pairs should be named in parallel, as `DesktopLanding` and `MobileLanding` are. A message-bus topic should carry the prefix of the component that actually publishes it.

For a naming finding, offer two or three alternatives with a recommendation, because Pete likes to choose names himself.

### Comments that tell the truth

Raise any comment that is false, stale, or orphaned in code the change touches. That includes comments the agent did not write, because Pete wants them gone regardless of who wrote them. Doc comments must state every effect a caller can observe, since he relies on them through editor hover help. For example, a function that also updates `VisibleArea` must say so.

The opposite fault matters too. A comment should exist only for a constraint the code cannot show. A field whose meaning persists across calls deserves one. Seven identical comments at seven call sites do not, because the reason belongs once, in the callee's doc comment.

### Separation of concerns and coupling

Pete thinks architecturally, and he cares about where knowledge lives as much as about names. The concern here is narrower than "single responsibility" or "decoupling" in general, and the boundary matters, because those labels invite exactly the findings he declines. A finding belongs here when knowledge crosses a boundary it should not. There are three ways that happens.

The first is a layer learning a concept that belongs to another. For each new field, method, parameter, or message, ask whether the package it lands in already had that concept. `PixelRatio` on the generic `Surface` interface was a leak, because only the HTML implementation knows about pixel ratios and the emulated surface had to fake one. The renderer testing `IsARay` was another, because rays are a selection concept and the renderer should only follow style. When data has to pass through intermediate layers, Pete prefers those layers not to understand it at all: his suggested alternative for render diagnostics was an opaque value whose contract is only between a renderer and the consumers of its metrics, or failing that a message on the bus.

The second is data distorted to fit someone else's mechanism. The drag-selection rectangle was drawn by inventing a diagonal line so that it could reuse the line background mask, and Pete called that a design smell. When a change shapes its data to suit an existing implementation rather than what the data means, raise it.

The third is a fact with more than one source of truth, whether in one repo or across `dxact-wasm` and `dxact-draw`. Pete insisted that the list of drawings in R2 that the product depends on must be defined in exactly one place.

Each concern should also sit with its natural owner, and the following cases of misplaced ownership have come up.

- An orchestration split between the orchestrator and its parts. The orchestrator that composes the floating coordinates had to own all of the backing rectangle, not share it with the nudge it composes.
- Settings-like constants defined outside the `settings` package, which is where the codebase keeps them.
- WASM learning details of persisted drawing storage, which the host owns.
- Cross-repo automation placed anywhere but `dxact-wasm`, which owns it.
- A specialised type placed in a generic package such as `geom`.

When a change solves a problem with a special case, consider whether a systematic mechanism would be more truthful. Pete replaced a controller-owned blacklist of commands with a flag that every command returns when it runs.

What does not belong here is rearranging code within a boundary that is already sound. Do not raise a finding such as "move `showRecipes` from the guidance shell into the sibling registry, so the shell is pure composition". Pete declined that one, because nothing crossed a boundary and nothing would get easier to change.

### First-time introductions

Flag any language feature, standard-library package, third-party dependency, or pattern that the codebase has not used before. Pete rejected Go's `reflect` for that reason alone. A first use should be a conscious decision, so the finding should say what was introduced, why it was used, and what the existing alternative would have been.

### Readability of the code itself

Pete wants the code to explain itself. Raise these cases.

- A function so long that its process is no longer visible. It should read as an orchestration of named helpers that can be unit tested. On a hot path, such as code that runs on every mouse move, the split must not cost performance.
- Control flow that is not semantically honest, such as an early return that hides the positive case where an inverted `if` around that case would state it. Idiomatic Go is the exception: error handling and guard-clause returns placed in sequence at the start of a function, before the main body, are the expected shape and not a finding.
- A construct that many developers would struggle to read, such as a dense regular expression, where plainer logic would do.
- A literal argument whose meaning is invisible at the call site. A named constant fixes it, as `includeEnds` replaced a bare `0` tolerance.
- A guard or condition that has no effect. That is a smell, and the finding should say what the code was presumably trying to do.

### Code volume and plumbing

Notice when a piece of state is passed as an argument through a chain of functions only because it lives somewhere those functions cannot reach. Moving it to its natural owner, where the readers can see it directly, often removes a lot of code. Pete made exactly this change to the rays-video nudge: `raysVideoEmbarked` had been passed into each function that needed it, and he had it held as WASM-side persistent state reflected as a field on the `Preview` object instead, which shrank the feature noticeably.

Flag dead code as well. Unused parameters matter twice, because they also fail the lint in `make allnative`. So do functions and tests whose callers the change removes, unless the plan schedules their deletion explicitly.

### Tests that earn their place

New behaviour should have a test, and a real edge case in the geometry or logic deserves one. Pete accepts a small refactor that isolates logic for unit testing, provided it does not muddle the code. He regards a test of a trivial constructor as noise unless the constructor does something non-trivial, so raise such tests as candidates for removal. Judge tests against the `test-*` skills for substance only, never for style.

### Correctness that is real

Genuine defects come first, naturally. Beyond those, report an arbitrary choice whose sufficiency is not obvious, such as taking one of the two directions along a line. Also report code that works only because of a fortunate side effect elsewhere, behaviour that drifts from the plan's stated intent, and a performance cost on a hot path.

Verify every finding before reporting it. Read the code path, check `main` when the history matters, and run a test when that settles the question. Pete was once misled by a review guide that asserted something it had inferred rather than seen, so each finding must rest on what the code demonstrably does.

### Opinions encoded in other skills

Pete's other skills encode further opinions, notably `go-coding`, `typescript-coding`, `procedural-task-entry-points`, `dedupe-preemptive`, and the `test-*` family. Apply them only when a violation is substantial enough to clear the bar described below. Do not turn them into a checklist.

## What Pete is content to risk

Leave the following out, even when the observation is true. Pete has declined to act on each of these kinds of point in past reviews, and including them only dilutes the findings that matter.

- Optional structural tidies within a sound boundary, as described at the end of the section on separation of concerns, including merging two lookup maps that are a fair split.
- Theoretical races and harmless edge cases on paths that do not occur in practice. Past examples include two clicks landing before an echo arrives, an idempotent echo on a no-op, a prop without a default whose only caller always passes one, and a single-writer field that could in principle be written elsewhere.
- Hypothetical future constraints, such as branch protection, additional consumers, migration for existing users, or old browsers. DrawExact is a solo project with no meaningful existing user base, nothing but `dxact-draw` consumes `dxact-wasm`, and old browsers are unsupported by product decision.
- Micro-performance away from hot paths, or where the compiler already removes the cost, as with an accessor that inlines.
- Formatting and lint-level style, which `gofmt`, `golines`, and the linters own.
- Praise. The verdict can say in a sentence that the change is sound, but there is no section on what is good.

A point in one of these areas still qualifies when it causes a real defect, misleads a reader, or contradicts a documented decision.

## The bar and the budget

Before including a finding, ask whether Pete would act on it or want to discuss it. If he would read it and move on, leave it out. Aim for three to five findings, and never exceed seven. When more candidates clear the bar, keep the ones that most affect correctness, a reader's understanding, and architectural ownership, in that order. Several instances of one pattern make one finding, not several.

Do not raise a symptom that the fix for another finding removes. A warning comment on a field, or a name that no longer fits, disappears when the field moves to its owner, so it belongs inside that finding's fix rather than beside it.

If nothing clears the bar, say so plainly. Never manufacture findings to make a review look thorough.

The opposite case also needs saying plainly. When the problems are too numerous to list without overwhelming Pete, the verdict should say that the change, or a named part of it, is a mess that needs serious attention. Then describe the dominant problems as a few themes, with one or two representative locations each, instead of listing every instance. A short review of a bad change is correct; it should not hide how bad the change is.

## Delivering the review

Write the review as a Markdown document in the repo, beside the plan or analysis document that the change implements, or in `dxact-wasm/docs/planning/` when there is none. Name it `<topic>-review-findings.md`. Follow the `ai-code-review` skill's link rules: paths relative to the document, no line fragments, and every link target checked before finishing. Follow the `markdown-guidelines` rule for the prose.

Pete must be able to hold each finding in his head after one reading. A finding that needs rereading has failed, however accurate it is, so readability outranks completeness of evidence.

Open with a short paragraph: the scope reviewed, by repo and commit range; the verdict; one sentence on whether anything casts doubt on correctness; and the most important finding. The verdict is one of four: the change is sound, it is sound with points worth acting on, it has a problem to fix before merging, or it needs serious attention because its problems are too numerous to list. Do not list what was checked and found fine.

Then give the findings as numbered sections, most important first, each in this shape:

```markdown
## 1. <A sentence stating the problem>

Kind: <familiar label>. Correctness: <unaffected | affected, and how>.

<One or two sentences on what is wrong and why it matters.>

Fix: <one or two sentences on the remedy, without writing the patch.>

Where: <links, with line numbers>.

Disposition: <fix now | discuss | debt>.
```

- Kind names the fault in terms Pete already maps to a remedy: separation of concerns, single-responsibility violation, duplication, leaky ownership, misleading comment, naming, dead code, plumbing, first-time introduction, missing test, or defect. The label describes a finding; the bar for raising one is still the narrower one set out above.
- The problem and the fix together stay within about 80 words.
- In the prose, refer to code by its role, such as "the family index", and keep identifiers to one or two per sentence. File names, identifiers and line numbers go in the Where line.
- Recommend one fix. Do not add a fallback such as "if that is more than you want, the smaller fix is". The exception is a naming finding, which offers two or three alternatives with a recommendation.
- Fix now is the default. Use discuss only when a decision is genuinely Pete's to make, and state that decision as one question in the Fix line. Use debt, meaning record it in `docs/backlog.md`, when the fix costs more than it is worth now; Pete deliberately carries some debt, so that is a legitimate outcome rather than a cop-out.

The numbering lets Pete triage with short replies such as `1: fix, 2: discuss, 3: debt`, or with `pch todo` remarks in the document. When he asks to discuss a finding, discuss it without changing code.

If Pete asks for a code review guide as well, produce it with the `ai-code-review` skill, and have the guide's review-focus section link to the findings document rather than repeat it.

Finish with a short chat message that links the document and restates the verdict.
