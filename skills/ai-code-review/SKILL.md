---
name: ai-code-review
description: >-
  Generate a code-review helper document for generated code.
---

# Objective

- To support a human who wants to review the changed code in newly generated code
- In the context of the project being open in an IDE like VSCode or Cursor

## When to use

When the human asks you to invoke this skill explicitly

## Deliverable

A review markdown document inserted into the repo being reviewed

## Code review topics to cover (where applicable)

- What was the reason for this code to be changed?
- What changed conceptually speaking
- What was the essence (not the detail) of the change made

## Code review document writing influences

- Help the reader survey the body of changed code:
  - in an order that aids comprehension
  - in chunks chosen also to aid the reader's education
- Point to relevant code using links that resolve to code in the IDE
- Don't supply fine details because the code itself does that
- Instead write the high level survey to guide the reader's inspection of the code
