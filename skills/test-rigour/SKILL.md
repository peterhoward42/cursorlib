# Cursor Skill: Robust Test Generation

## Intent
Generate tests with one source of truth.
Expected results must follow mechanically from the scenario.

Model every test as:

Given: explicit domain facts
When: one action under test
Then: a consequence of those facts

The Then must follow from the Given. Never invent it independently.

---

## Default Pattern (Use First)

fixtures -> derive expected -> assert

Example:

events = [deposit(50), withdrawal(20)]
expected = sum(events)
assert balance(events) == expected

---

## Fixture Rules

1. Fixtures define the world. They are the only source of truth.

2. Express fixtures as domain facts, not mutation.

Good:
events = [deposit(50), withdrawal(20)]

facts = [
  orderPlaced(t1),
  orderCancelled(t2),
  refundIssued(t3)
]

Bad:
account.balance = 0
account.balance += 50
account.balance -= 20

3. Prefer:
- event lists
- records / tuples
- ordered facts where time matters

4. Avoid meaning encoded through sequential edits.

---

## Assertion Rules

Prefer derived oracles.

Compute expected results from fixtures using a small local rule.

Good:

events = [deposit(50), withdrawal(20)]
expected = sum(events)
assert balance(events) == expected

Hard-coded expectations are allowed only if:

- the value is trivial from the fixture, or
- the test proves the fixture entails it.

Otherwise do not hard-code expected values.

---

## Property Tests (Allowed)

Use when correctness is best expressed as invariants.

Example:

sorted = sort(values)

assert is_sorted(sorted)
assert same_elements(values, sorted)

---

## Generation Procedure

1. Identify the domain facts.
2. Write the Given from those facts.
3. Isolate one action for the When.
4. Choose one Then form:

- derived oracle
- checked hard-coded oracle
- property test

5. Reject the test if fixtures and expectations could drift independently.

---

## Rejection Rules

Do NOT generate tests where:

- the expected result is a guess not tied to fixtures
- scenario meaning is encoded through mutation
- fixtures and assertions encode the same intent separately
- expected values are hard-coded without derivation or entailment
- the oracle duplicates the production algorithm

---

## Smell Check

Rewrite the test if any answer is yes:

- Could fixtures change without changing the assertion?
- Is the scenario hidden in object mutation?
- Is the expected result an independent guess?
- Is a number hard-coded without proof from the fixture?
- Is the oracle large enough to duplicate production logic?

---

## Operative Rule

Write tests with one source of truth.

Given = explicit domain facts.
When = one action.
Then = derived consequence of the Given.

Prefer facts over mutation and derivation over hard-coded expectations.
