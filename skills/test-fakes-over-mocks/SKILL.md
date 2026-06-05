---
name: test-fakes-over-mocks
description: >-
  Prefer dedicated fakes over mock libraries when substituting dependencies in
  tests. Use when writing, reviewing, or refactoring tests that need test
  doubles, stubs, or substitutes for collaborators.
---

# Cursor Skill: Fakes Over Mocks

## Intent

Programmatic tests in nearly all languages benefit from substitutes for real
dependencies. Use **fakes**, not **mocks**.

---

## Definitions

### Mock

A **mock** is the use of a code library or package that offers generic support
for making things that pretend to be something else, or can be used in the place
of something else, and often but not always provide some visibility after their
use of what they experienced — which is often useful to assert on in a test.

Examples to reject:

- `jest.mock`, `sinon`, `unittest.mock`, `gomock`, `mockito`, `nock` (when used
  as a generic stand-in rather than a dedicated fake HTTP server type)
- `expect(...).toHaveBeenCalledWith(...)` on library-generated stand-ins
- `On("Method", ...).Return(...)` style generated doubles
- Any generic "create a pretend object for interface X" tooling

### Fake

A **fake** is a dedicated body of code that offers to pretend to be something
else — but in this case, it pretends to be **one particular thing**. Instead of
being a Duck it is a deliberately designed fake Duck.

Examples to prefer:

- `FakeUserRepository` with real methods, real signatures, and explicit in-memory
  behaviour
- `RecordingMailer` that stores sent messages in a slice the test can read
- `FixedClock` that returns a configured instant
- A small in-memory `OrderStore` used only in tests

---

## Core Principle

**Prefer fakes over mocks.**

Substitute artefacts should be:

- named so they document their role
- implemented with real methods on real types
- navigable: a developer can jump to the fake and read what it does

This makes tests easier to read, understand, and debug. The trade-off is a
little more coding work — accept that cost.

---

## When to Apply

Use this skill whenever test code needs to replace a collaborator, external
service, clock, random source, repository, client, or other dependency.

Before adding a new fake, check whether the repository already has one for the
same role (`dedupe-preemptive`).

---

## How to Write Fakes

1. **Name for intent** — e.g. `FakePaymentGateway`, `InMemorySessionStore`,
   `RecordingEventPublisher`. The name is part of the test documentation.

2. **Implement the real contract** — satisfy the interface or behavioural role
   the code under test expects. Methods exist with the correct names and
   signatures.

3. **Keep behaviour explicit** — use fields, slices, maps, or simple counters
   the test can inspect after the action. Prefer reading observable state over
   library call-verification APIs.

4. **Colocate with tests** — put fakes in test helper files, `testing`
   packages, or `*_test.go` / `__tests__` support files unless the project
   already has a shared fake location.

5. **One fake per substituted thing** — design for the specific collaborator,
   not a generic reusable mock factory.

---

## Generation Procedure

When generating a test that needs a substitute:

1. Identify the collaborator's contract (interface, type, or behavioural role).
2. Search the repo for an existing fake with the same role.
3. If none exists, write a small dedicated fake type with explicit behaviour.
4. Construct a fresh fake per test (see `test-isolation`).
5. Run the action; assert on returned values and on state the fake recorded.

---

## Rejection Rules

Do NOT generate tests that:

- import or configure mock libraries or generic mock generators
- use `jest.mock`, `sinon.stub`, `gomock.NewController`, `unittest.mock`,
  `mockito`, or equivalent
- verify interactions through library-specific "was this called?" APIs when a
  readable fake field or collection would do
- hide substitute behaviour inside framework setup instead of named fake types

---

## Smell Check

Reject or rewrite the test if any answer is yes:

- Is a mock library doing the pretending instead of a named fake type?
- Can the developer not navigate to a method body to see what the substitute
  does?
- Is the substitute generic ("any interface") rather than specific ("this
  repository")?
- Are assertions expressed only through mock-framework call expectations with no
  readable recorded state?

---

## Operative Rule

When generating test code, adopt fakes. **Do not use mocks.**
