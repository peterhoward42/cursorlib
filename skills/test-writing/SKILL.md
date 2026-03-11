---
name: test-writing
description: Write well-scoped tests for named functions, validators, handlers, and application services, using tests-rigour and test-isolation.
---

# test-writing

This skill is for writing tests.

Tests must be designed according to:
- `tests-rigour`
- `test-isolation`

## Instructions

When asked to write tests:

- Determine the appropriate test level for each named target
- Prefer the narrowest test scope that meaningfully verifies the behaviour
- Test the responsibility of the named target, not the internals of its dependencies
- Avoid duplicating lower-level assertions in broader tests unless the broader test proves composition, boundary behaviour, or another distinct concern
- Prefer observable behaviour over implementation detail
- Cover happy path, edge cases, invalid input, and failure handling where relevant
- Keep tests independent, readable, and explicit in intent
- State assumptions briefly when the code is not shown

## Guidance by target type

### Pure functions
Write unit tests for:
- expected outputs
- edge cases
- invariants
- invalid arguments if part of the contract

### Validation logic
Write focused tests for:
- valid payloads
- missing required fields
- wrong field types
- malformed nested objects
- invalid combinations
- unknown fields when relevant

### Application or orchestration methods
Write tests for:
- interaction with collaborators
- control flow and sequencing where relevant
- returned results
- side effects
- propagated or translated failures
- idempotency or duplicate suppression where relevant

Do not re-test the internal logic of collaborators already covered by their own tests.

## Output format

Provide:
1. a short test plan
2. the test code
3. a brief assumptions note if needed
