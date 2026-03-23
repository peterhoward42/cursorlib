# Skill: Shorten Overlong Names in JavaScript and TypeScript

Purpose:
Rename overlong files, directories, and source-level symbols in JavaScript and TypeScript so they become shorter, clearer, and more natural, while preserving meaning and consistency.

This skill is for codebases where names have become too long because they try to encode too much context directly into each name. The goal is to let surrounding context do more of the explanatory work.

## Scope

Apply this skill to:
- JavaScript and TypeScript source files
- file names
- directory names
- exported and non-exported symbols
- functions
- classes
- interfaces
- types
- variables
- constants
- enums
- React components
- hooks
- related test files when they follow the same naming pattern

Do not apply this skill outside JS/TS unless explicitly requested.

## Core principle

Do not shorten names mechanically.
Shorten them intelligently.

A good rename removes redundant context that is already supplied by:
- the containing directory
- the file name
- the module boundary
- the type context
- nearby naming conventions
- the role of the symbol in the local code

Names should not carry every detail themselves when the surrounding structure already supplies part of the meaning.

## Length targets

Use these as heuristics, not rigid rules.

### Symbol names
- Preferred target: 18 characters or fewer
- Soft maximum: 28 characters

### File and directory names
- Preferred target: 16 characters or fewer per path segment
- Soft maximum: 24 characters per path segment

### Test names
Be more permissive.
Longer names are often acceptable for tests when they improve clarity of intent.

Suggested guidance:
- Preferred target: 28 characters
- Soft maximum: 40 characters

A name above the soft maximum should normally be shortened unless there is a strong reason not to.

## What to remove

Prefer removing wording that is redundant in context.

Common sources of redundancy:
- repeating the directory concept inside file names
- repeating the file concept inside symbol names
- repeating framework or domain words that are already obvious nearby
- repeating words like `data`, `pipeline`, `service`, `manager`, `handler`, `processor`, `utility`, `helper`, `component` when the context already supplies them
- stacking multiple near-synonyms into one long name
- names that read like concatenated summaries rather than natural identifiers

Example:
- in `data-pipelines/`, avoid names that also repeat `DataPipeline`
- in `user-profile/`, avoid every file and symbol repeating `UserProfile`
- in a file already named for a concept, avoid giving the main export the full file concept again unless needed

## Consistency rules

When you find a long naming pattern shared across related artifacts, rename the whole family consistently.

Typical family:
- source file
- main export in that file
- related helper names
- related types
- related test file
- imports of those names elsewhere

Keep naming aligned across that family unless there is a clear reason not to.

Example pattern:
- `processIncomingCustomerDataPipeline.ts`
- `processIncomingCustomerDataPipeline()`
- `processIncomingCustomerDataPipeline.test.ts`

These should usually be shortened together around the same core name.

## Exception for tests

Be careful with tests.

Do:
- keep descriptive test case strings long when needed
- allow test file names to remain somewhat more explicit than production file names
- preserve clarity about behavior under test

Do not:
- aggressively compress test descriptions into vague short names
- make tests harder to scan just to satisfy a length target

Where a test file mirrors a production file, keep the relationship obvious, but still consider dropping redundant contextual words.

## Rename strategy

For each candidate rename:

1. Identify the real semantic core of the name.
2. Identify which words are already supplied by context.
3. Remove redundant words first.
4. Prefer plain, natural, readable names over abbreviations.
5. Keep enough distinction to avoid collisions with nearby names.
6. Apply the rename consistently across related files and symbols.
7. Verify imports, exports, references, and type usage all still line up.

## Preferred naming style

Prefer:
- shorter natural words
- one strong concept over several stacked qualifiers
- names that make sense when read in their local context
- conventional JS/TS naming patterns

Avoid:
- cryptic abbreviations
- unnecessary truncation
- compressed names that lose semantic shape
- renames that create ambiguity with nearby concepts

## Context-first examples

Example 1:
Directory:
- `data-pipelines/`

Before:
- `customerDataPipelineTransformer.ts`
- `customerDataPipelineTransformer()`

Possible after:
- `customerTransformer.ts`
- `customerTransformer()`

Reason:
`data pipeline` is already supplied by the directory context.

Example 2:
Directory:
- `billing/invoice-generation/`

Before:
- `invoiceGenerationScheduler.ts`
- `scheduleInvoiceGeneration()`

Possible after:
- `scheduler.ts`
- `scheduleInvoices()`

Reason:
`invoice generation` is already strongly present in the path.

Example 3:
File:
- `userSummary.ts`

Before:
- `buildUserSummaryData()`

Possible after:
- `buildSummary()`

Reason:
inside `userSummary.ts`, both `user` and `summary` may already be partially supplied by context.

## Safety checks

Do not rename in ways that:
- break public APIs without clear intent
- obscure domain-important distinctions
- collapse two distinct concepts into one name
- remove wording that is needed to distinguish behavior
- create conflicts with existing files or symbols
- make grepability materially worse for important concepts

Be especially cautious with:
- exported library APIs
- widely used shared types
- generated code
- framework-constrained filenames
- config-driven file naming conventions
- test snapshots or string-based references

## Decision rule

When deciding whether to shorten a name, ask:

"Which parts of this name are doing real local work, and which parts are only repeating context I already get from the path, file, module, or surrounding code?"

Only keep the parts doing real local work.

## Output behavior

When applying this skill:
- identify overlong names
- propose shorter replacements
- explain what context makes the removed words redundant
- rename related files and symbols consistently
- preserve correctness across imports, exports, tests, and references
- keep tests readable, even when they remain longer than production names

Default bias:
Prefer clear, compact names that rely on context rather than overexplaining themselves.
