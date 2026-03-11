---
name: semantic-rename-auditor
description: Detects names that have become semantically misleading as responsibilities evolved, then autonomously renames them in small batches while keeping the Go repository test-clean. Performs semantic correction only, never architectural refactoring.
---

# Semantic Rename Auditor

## Purpose

Audit the repository for **semantic drift in names**.

A name may have been correct when introduced but become misleading as the artifact's responsibility evolved. When that happens, rename the artifact to reflect its current role and propagate the rename consistently.

This skill performs **semantic correction through renaming only**.

It does **not** perform architectural refactoring.

## Activation

Use this skill when the user asks to:

- audit names
- check semantic drift
- improve naming accuracy
- rename misleading artifacts
- run a semantic rename pass
- align artifact names with current responsibilities

## Core Principle

Rename only when the current name would cause a competent reader to form a **meaningfully incorrect expectation** about the artifact's responsibility.

This is semantic repair, not aesthetic cleanup.

## Non-Goals

Never:

- split or merge artifacts
- recommend decomposition, extraction, or restructuring
- redesign architecture
- change program behavior
- rename purely for elegance, brevity, symmetry, or style
- invent new domain vocabulary unnecessarily

If a rename would require architectural judgment, skip it.

## Target Artifacts

Primary scope:

- package names
- directory names with domain meaning
- file names
- types and interfaces
- exported functions
- unexported functions with significant domain roles
- methods
- handler functions
- test names tied to renamed artifacts
- naming-sensitive comments and docstrings

Secondary scope, only with strong evidence:

- route paths
- config keys
- environment variables
- database identifiers
- event names

Ignore unless explicitly requested:

- local variables
- parameters
- short helper temporaries

## What Counts as Semantic Drift

Rename when the name is any of the following:

### Too narrow

The name implies a single task but the artifact now performs multiple roles.

Example:
`Ingest` now ingests data and also serves reports.

### Too broad

The name is generic but the artifact now performs a specific domain task.

Example:
`Utils` now only handles storage path normalization.

### Historically stale

The name reflects an earlier implementation phase but not the current role.

Example:
`LegacyUploadBridge` is now the primary endpoint.

### Role mismatch

The name implies the wrong conceptual role.

Example:
`Parser` now validates, enriches, persists, and reports.

### Domain mismatch

The surrounding codebase clearly uses a better domain term than the artifact's current name.

## Naming Principles

Prefer:

- names that reflect current responsibility
- vocabulary already present in the repository
- domain nouns when responsibilities have broadened
- names likely to remain valid if the artifact grows slightly further in the same direction
- clarity over cleverness

Avoid:

- vague generic words such as `Manager`, `Processor`, `Service`, or `Handler` unless that idiom is already clearly established in the repository
- invented terminology not already supported by nearby code
- churn for minor improvements

## Decision Rule

Rename automatically only if all of the following are true:

1. the current name is materially misleading
2. a clearly superior replacement exists
3. the replacement aligns with repository vocabulary
4. the rename can be propagated mechanically
5. behavior remains unchanged

If multiple good replacements exist and no single one is clearly superior, do not rename automatically.

## Evidence Sources

Use:

- implementation
- call sites
- imports and dependencies
- sibling files and packages
- tests
- comments and docstrings
- route or handler behavior
- surrounding domain vocabulary

Do not base renames on a single superficial clue.

## Execution Workflow

### Step 1: Scan

Inspect the repository for candidate artifacts whose names may have drifted.

For each candidate, infer:

- what the current name implies
- what the artifact actually does now

Record candidate mismatches.

### Step 2: Evaluate

For each candidate:

1. determine whether the mismatch is material
2. search the repository for better domain vocabulary
3. identify the strongest replacement candidate

If no replacement is clearly superior, skip the rename.

### Step 3: Plan a Rename Batch

Prepare a **single semantic rename batch** consisting of one conceptual rename and its direct fallout, such as:

- primary artifact rename
- declaration updates
- reference updates
- import updates
- related file renames
- related test renames
- nearby naming-sensitive docstring or comment updates

Do not mix unrelated renames in the same batch.

### Step 4: Apply the Rename

Perform the rename consistently.

Update:

- symbol declarations
- call sites
- imports
- filenames if repository convention ties filenames to responsibility
- related tests
- comments and docstrings where the old term would now mislead a reader

Do not change logic.

### Step 5: Restore Repository Correctness

After each batch:

1. run formatting or import cleanup if necessary
2. run full repository validation

Preferred validation command:

`go test ./...`

If tests fail:

- repair mechanical fallout from the rename
- update missed references
- fix imports
- correct affected tests

Continue until the repository returns to a clean buildable, test-passing state.

Never proceed to the next batch while the repository is broken.

### Step 6: Continue

Repeat the batch cycle for the next high-confidence rename.

Stop when no remaining candidates exceed the confidence threshold.

## Safety Rules

Always maintain these constraints:

- the repository must return to a clean `go test ./...` state after each batch
- never stack multiple unresolved rename batches
- never modify behavior
- never introduce new abstractions
- never silently change public or external contracts unless the user explicitly included those in scope

If a rename requires design judgment beyond naming, skip it.

## Confidence Levels

### High confidence

Apply automatically.

Typical signs:

- clear semantic mismatch
- obvious replacement vocabulary already present in the repository
- rename is mechanical
- behavior remains unchanged

### Medium confidence

Report but do not rename.

Typical signs:

- multiple plausible replacement names
- domain vocabulary is inconsistent
- artifact responsibility is ambiguous
- rename touches external or public surfaces whose full consequences may not be visible

### Low confidence

Ignore.

## Output Report

At the end, produce a concise ledger with two sections.

### Applied renames

For each applied rename, report:

- old name
- new name
- artifact type
- short reason
- confidence
- files affected

Example format:

- old name: `Ingest`
- new name: `RecordsHandler`
- artifact type: HTTP handler
- reason: now both stores records and produces reports
- confidence: high
- files affected: 6

### Detected but not applied

For each skipped case, report:

- artifact
- current name
- reason for drift
- possible replacements, if useful
- why it was not applied

## Behavior Philosophy

Act with restraint.

A successful run is not one that renames many things.

A successful run is one that renames **only the artifacts whose names materially mislead readers**.

## Operational Motto

Rename to match current responsibility.

Do not redesign the system.

Keep the repository green after every change.
