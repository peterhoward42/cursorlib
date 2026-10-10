---
name: ai-code-review
description: >-
  Write a code review guide for newly generated code: a Markdown document in
  the repo that explains why the code changed, what changed conceptually, and
  the order in which to survey it, and that says what was verified and what
  remains open, so that it can stand in for reading the code. Use only when
  the user asks for a code review guide or names this skill. Not for a review
  with findings, which is the code-review-findings skill.
---

# Code review guide

A code review guide helps a human review code that an agent has just written, with the project open in an IDE such as Cursor. Pete often finds that a good guide tells him enough that he does not open the code at all. Write every guide expecting that: it should stand in for the code wherever it can, and say plainly where it cannot.

## Where the guide goes

Write the guide as a Markdown document in the repo being reviewed, beside the plan or analysis document that the change implements, and name it `<topic>-review.md`.

## What the guide covers

Open with the scope. Say which repos and files changed, whether the changes are committed, and which areas of the product are untouched. Then cover, where they apply, why the code changed, what changed conceptually, and the essence of the change rather than its detail. Link the plan or issue that asked for the change rather than restating it.

## Survey the code in a helpful order

Most of the guide walks the reader through the changed code. Order the walk so that each part makes sense given the parts before it, and choose the chunks so that the reader learns how the change is built as they go. Keep to the high level, because the code carries the detail. For each chunk, say what the code is for and what to look at, then link to it.

## Write it to stand in for the code

The guide is written by the agent that wrote the code, so it naturally describes what the code was meant to do. A reader who does not open the code cannot tell intention from fact, so describe only what you have checked the code actually does, and mark anything you have not checked as unchecked. Do not offer speculation as a reason for the change.

The code cannot tell a reader how it was tested or what was decided along the way, so the guide carries that too. Include the following sections after the survey.

- **Verification done.** What was run and what was observed, including the devices, modes, or environments covered. Then what was not exercised, so the reader can judge the risk that remains.
- **Open items for the reviewer.** Decisions taken during the work that the plan did not settle, and any place where the code departs from the plan's wording, each with its reason. Known gaps, interactions with later planned work, and anything you are unsure of.

When the correctness of a change rests on something that a description cannot vouch for, such as a layout constraint, a subtle condition, or an ordering assumption, say so in the survey, and name that place as the one worth reading if the reader reads any code at all.

## Links to code

Point to the code with links that resolve in the IDE.

- Use Markdown links with a path relative to the review document, for example ``[`nameColumn.js`](../../src/cpts/mydrawings/nameColumn.js)``.
- Never append a line fragment such as `#L16` or `#L16-L20`, because Cursor does not resolve a relative link that carries one. Give line numbers in the prose beside the link instead, for example "`nameColCh` (line 16)".
- Never use workspace-rooted paths with a leading `/`, because they do not resolve.
- Before finishing, check that every link target exists relative to the document, and that every line number given in the prose still points at what it names.
