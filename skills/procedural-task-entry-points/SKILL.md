---
name: procedural-task-entry-points
description: >-
  Prefer procedural application-task entry points over continuation-registration
  gates for linear user journeys (consent, confirm, connect, optional precondition
  then work). Invoke whenever a design would register pending/afterGrant-style
  callbacks into a shared offer/proceed orchestrator. Language-agnostic; motivated
  by JavaScript/TypeScript UI flows. Exception: when the story itself is a DRY
  wrapping orchestrator (e.g. token/async wrappers).
---

# Procedural task entry points

## Invariant

For a concrete application-level user task, **that task owns the story**. A reader
should understand the feature by reading one entry-point procedure—not by
reconstructing a registration protocol across a shared gate.

## When to apply (always)

Load and apply this skill whenever the default design is turning into (or already
is) the anti-pattern below: callers stuff continuations into a shared
offer/proceed/pending-action helper that later resumes them.

Typical smells: `offer*` + `proceed*` + pending/parked action bags; `afterGrant` /
`onContinue` registered far from the work; module-scoped “pending” so a dialog
knows what to run; entry points that only build callback structs.

## Preferred shape

1. **One entry point per concrete task** (named for the user intent).
2. Body is **procedural**: if precondition unmet → seek agreement; on decline →
   abandon; on agree (or already satisfied) → **run the work**.
3. Shared code is a **thin subroutine** (“seek consent if needed”), called *from*
   the entry point—not a framework that owns grant, resume, and “what next.”
4. Dialogs / prompts take **closures defined at or next to the entry point**
   (e.g. `onAgree` / `onDecline` via explicit dialog data props)—not a deferred
   action bag owned by a gate module.
5. After agreement, run the work **unconditionally** (precondition stays outside).

## Anti-pattern (reject for linear task + gate journeys)

- Register a pending action; shared proceed resumes it.
- Entry points only construct callback structs and call `offer*` / `run*`.
- One module both gates **and** performs session/grant side effects **and**
  invokes the caller’s continuation.
- Hidden module-scoped pending state required for the UI to know the action.
- Renaming bag fields while leaving inverted control—and calling that done.

## Exception: when the wrapping orchestrator *is* the story

**Sometimes** a shared wrapping orchestrator *is* the right design—specifically
when the product story **is** that DRY wrap for every call site (same mechanical
envelope around many operations), not “one user task with an optional gate.”

Example (JavaScript calling Google Drive): many Google Drive API operations each
need the same intervention—obtain an OAuth access token (possibly showing Google’s
account/consent UI), adapt a callback-based token API into async/await, then invoke
the given Google Drive operation with that token. A single wrapper that always does
that envelope is appropriate: callers are not registering a product journey; they
are opting into a **uniform infrastructure wrap**. That inversion is intentional
and legible.

Use the exception when:

- Every (or nearly every) call site needs the **same** mechanical envelope.
- The wrapper’s responsibility is stable and narrow (obtain token, retries, logging,
  callback→async bridge)—not “resume *your* feature after *your* consent dialog.”
- Reading the wrapper documents the shared mechanism; reading each call site still
  documents *which* operation runs.

Do **not** use the exception to justify a product-level consent/confirm gate that
steals ownership of heterogeneous user tasks.

## Language

Rules are **language-agnostic**. The motivating incident was JavaScript/TypeScript
UI + dialog `data` props; apply the same ownership test in Go, Python, etc.

## Related skills

- Composition-root ownership for HTTP: `http-handler-dependency-injection`
- Explicit data flow (necessary, not sufficient): `typescript-coding`
- Structural SoC: `refactoring`
