
---
name: test-uniformity
description: Some ways to leverage uniformity and standards in tests in the
interests of making them easier to read and to avoid some common mistakes.
---

## When to apply this skill

- Whenever writing test code

## 1. Avoid mixed language syntaxes

### Context

- A common coding phenomenon in programming is to use to use the language's
  string literals to express some content in another "language"
- The canonical example is to write some JSON syntax inside a language-native
  string literal.
- The concept is equally true for other DSLs, for example YAML or SQL.
- It is difficult for LLMs to reliably reconcile the escaping and 
  extrapolation / interpolating syntax for two such language  syntaxes used in 
  in overlapping places. 
- This rule avoids it systemically

### The rule
- Do not mix or overlap languages in this way
- Do not use string literals to define DSL fragments or content except for
  extremely simple cases.
- Do find alternatives for generating the required DSL
- The canonical way is to build a structural representation of the data, and
  then to use a dedicated serialiser of some kind to generate the DSL text.
- An example for the Go language would be to define and build a structure or a
  map and then to JSON.Marshal it to produce the string output required.

## 2. Use DRY helpers to build inputs and payloads for tests

### Context

- It is a common requirement in tests to provide some input data for the
  code under test. Often this is a paylod type data.
- Often a canonical or default payload will be required by many test cases.
- Often a malformed or somehow special payload is required for tests
- Using DRY code to construct inputs and payloads for tests makes the code
  easier to read, to reason over, to debug, and to change.

### The rule

- Use DRY constructors or factories to produce input data and payloads for
  tests whenever possible and practical.
- When malformed or otherwise special payloads or inputs are required, start by
  generating a valid item as above, and then programmatically mutate it to
  introduce the malformed aspect or special aspect.

### Isolation

- Each test (and each case in a table-driven or parameterised test) must
  obtain its own instance from the helper—e.g. call the factory inside the test
  or inside the loop. Do not create one shared instance before a loop and reuse
  it across cases; that violates test isolation (fresh fixtures per test).
