---
summary: Guidance for composing and refactoring TypeScript and JavaScript
application code, focusing on clear design, honest signatures, useful
encapsulation, and avoiding unnecessary abstraction.
---


# TypeScript for Application Code

This skill guides code generation and refactoring for **TypeScript and JavaScript application code**, not public libraries. The aim is to produce code that is easy to read, easy to trace, easy to change locally, and honest about what really varies.

The default bias is toward **clarity over flexibility**, while still preserving:
- separation of concerns
- low coupling between subsystems
- useful encapsulation
- interface-based seams where they materially help testing or boundaries
- type information where it clarifies the code rather than merely making it more formal

## Core stance

Write code for the system that actually exists.

Do not introduce generality unless there is a concrete need for it in the application. A small amount of duplication is often better than premature abstraction.

Prefer code that lets a reader quickly answer:
- What does this function or class need?
- What does it return or change?
- What calls it?
- What is genuinely variable here?
- Where is the state and who owns it?
- Which boundaries matter?

## Primary design doctrines

### 1. Keep signatures honest

A function should require the inputs it conceptually needs.

- Do **not** make parameters optional just because TypeScript allows it.
- Do **not** hide missing required information behind fallback logic inside the function.
- Use defaults only when the default is a real part of the function's meaning.

Good:

```ts
function formatPrice(amount: number, currency = 'GBP'): string
