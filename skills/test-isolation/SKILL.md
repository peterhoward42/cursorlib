# Cursor Skill: Test Isolation and Determinism

## Intent
Every test must run in a **fresh, isolated world**.

The result of a test must not depend on:
- other tests
- execution order
- shared mutable state
- system time
- randomness
- external processes

A test must pass whether it runs:
- alone
- before or after any other test
- repeatedly
- in parallel

---

## Core Principle

A test must behave as if it is the **only test in the process**.

If running the full test suite in a different order could change the result, the test is invalid.

---

## Isolation Rules

### 1. No Shared Mutable State

Tests must not modify shared global state.

Avoid:

- global variables
- shared singletons
- static mutable data
- module-level mutation
- cached state that persists across tests

If global state exists, reset or isolate it inside the test setup.

---

### 2. Fresh Fixtures Per Test

Each test must construct its own world.

Do not reuse objects across tests.

Bad:

sharedUser = createUser()

test1 uses sharedUser  
test2 mutates sharedUser

Good:

test1 creates its own user  
test2 creates its own user

#### Table-driven and parameterised tests

Treat **each test case** (each row, each subtest, each parameter combination) as a separate test for isolation purposes.

- Each case must get a **fresh fixture**; do not create one fixture before the loop and reuse it across cases.
- Create the fixture **inside** the loop (inside each `t.Run`, `@ParameterizedTest` iteration, `pytest` parametrized case, etc.), so each case constructs its own world.
- Copying a shared "base" object in the loop (e.g. `ev := base` then mutate `ev`) still counts as reusing: the shared base is the reused object. Call the factory or constructor inside the loop instead.

Bad (shared base across cases):

```go
base := validFixture()
for _, tc := range cases {
    t.Run(tc.name, func(t *testing.T) {
        ev := base   // reuse: same base for every case
        tc.mutate(&ev)
        ...
    })
}
```

Good (fresh fixture per case):

```go
for _, tc := range cases {
    t.Run(tc.name, func(t *testing.T) {
        ev := validFixture()   // fresh for this case
        tc.mutate(&ev)
        ...
    })
}
```

---

### 3. No Order Dependence

Tests must not rely on execution order.

Reject tests that require:

- a previous test to populate data
- side effects from earlier tests
- implicit cumulative state

Each test must fully define its own setup.

---

### 4. Control Time

Tests must not depend on the real clock.

Avoid:

- current system time
- real delays or sleeps
- timing races

Instead use:

- injected clocks
- fixed timestamps
- simulated time

---

### 5. Control Randomness

Tests must not rely on uncontrolled randomness.

Allowed approaches:

- fixed seeds
- deterministic generators
- explicit values

Reject tests that rely on random behaviour without control.

---

### 6. Avoid External Dependencies

Tests should not rely on external systems.

Avoid:

- network calls
- real databases
- filesystem state
- environment configuration
- external services

Prefer:

- in-memory substitutes
- fakes
- deterministic fixtures

---

### 7. Parallel Safety

Tests must be safe to run concurrently.

Avoid shared resources such as:

- files with fixed names
- ports
- global registries
- shared caches

Use unique or isolated resources per test.

---

## Setup and Teardown Guidance

Prefer **constructing a clean world** over cleaning up a dirty one.

Good:

create fresh objects per test

Avoid:

mutating global state and attempting to restore it later

Teardown should only exist for unavoidable resources.

---

## Generation Procedure

When generating a test:

1. Assume no prior tests exist.
2. Construct the complete world within the test.
3. Avoid shared objects.
4. Control time and randomness.
5. Avoid external dependencies.
6. Ensure the test can run in parallel safely.

---

## Rejection Rules

Do NOT generate tests that:

- rely on global mutable state
- depend on previous tests
- assume execution order
- depend on real time or delays
- rely on uncontrolled randomness
- interact with real external systems
- reuse mutable objects across tests
- use a single shared fixture for multiple cases in a table-driven or parameterised test (create fixture inside the loop per case)

---

## Smell Check

Reject or rewrite the test if any answer is yes:

- Could another test change the outcome?
- Does the test rely on a previous test's setup?
- In a table-driven test, is one fixture created before the loop and reused for every case?
- Does it depend on system time?
- Does it depend on randomness without a fixed seed?
- Does it modify global state?
- Does it interact with external services?

---

## Operative Rule

A valid test must behave identically when:

- run alone
- run repeatedly
- run in any order
- run in parallel

Tests must construct their own isolated world and leave no persistent side effects.
