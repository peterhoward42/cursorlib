---
name: Thorough Removal
description: Use when removing, deleting, retiring, replacing, simplifying, or decommissioning code, features, components, dependencies, APIs, routes, configuration, or behaviour.
---

# Thorough Removal

When asked to remove something, treat the task as a complete excision rather than a minimal patch.

The goal is not merely to make the target disappear. The goal is to leave the repository in a cleaner, more coherent state after the removal.

## Core Principle

Prefer repository clarity, honesty, and coherence over minimising the size of the diff.

A slightly larger cleanup is usually preferable to leaving behind misleading remnants, obsolete abstractions, compatibility shims, dead pathways, or historical artefacts.

## Removal Process

After identifying the item to be removed:

1. Remove the requested item completely.
2. Trace all consequences of the removal.
3. Remove anything that now exists solely because of the removed item.
4. Simplify any interfaces, types, APIs, or structures that were supporting the removed functionality.
5. Leave the remaining code expressing the new reality as clearly as possible.

Do not stop once the immediate target has been deleted.

## Hunt for Orphans

Actively search for and remove:

* Unused imports
* Unused variables
* Unused constants
* Unused types
* Unused interfaces
* Unused props
* Unused parameters
* Unused return values
* Unused callbacks
* Unused events
* Unused state
* Unused selectors
* Unused routes
* Unused configuration
* Unused feature flags
* Unused assets
* Unused tests
* Unused fixtures
* Unused mocks
* Unused documentation
* Unused comments
* Dead branches
* Dead code paths
* Obsolete abstractions

Follow dependency chains until the repository reaches a stable state.

## Prefer Honest Interfaces

When functionality disappears, update interfaces to reflect reality.

Prefer:

* Removing parameters rather than making them optional
* Removing props rather than ignoring them
* Removing return values rather than leaving unused fields
* Removing branches rather than leaving dormant paths
* Removing configuration rather than leaving no-op settings

Do not preserve obsolete API shapes simply to reduce the amount of code that must change.

If callers must be updated, update them.

## Respect Language Discipline

In strongly checked languages, lean into the compiler, type system, linter, and tests.

Treat compiler errors, type errors, linter warnings, and unused-code reports as guidance for cleanup.

In dynamic languages, apply the same discipline manually.

Do not leave:

* Optional arguments that are no longer needed
* Default values that only support removed behaviour
* Ignored callbacks
* Placeholder parameters
* Compatibility branches with no remaining purpose

Aim for the same cleanliness that a strict compiler would encourage.

## Do Not Invent Legacy Requirements

Do not assume the existence of:

* Legacy users
* Legacy clients
* Persisted historical data
* Backwards compatibility requirements
* Migration obligations
* External integrations
* Public API consumers

unless there is concrete evidence for them.

The mere possibility of old data or old consumers is not sufficient reason to retain compatibility code.

## Evidence That Compatibility Matters

Treat compatibility as important when there is explicit evidence such as:

* Existing persisted data structures
* Migration code
* Versioned APIs
* Public interfaces
* Existing consumers
* Documentation requiring compatibility
* Tests explicitly validating legacy behaviour
* User instructions requiring preservation

If such evidence exists, preserve compatibility intentionally and document the reason.

Otherwise, prefer removal and simplification.

## Avoid Archaeological Layers

Do not leave behind:

* Compatibility shims
* No-op wrappers
* Temporary adapters
* Empty extension points
* Reserved parameters
* Future-proofing hooks
* Historical comments
* "Just in case" code

unless they are actively serving a demonstrated purpose.

The repository should not contain clues about removed functionality when those clues no longer provide value.

## Completion Check

Before considering the task complete, ask:

* What became redundant because of this removal?
* What interfaces can now be simplified?
* What assumptions can now be tightened?
* What compatibility code no longer has a reason to exist?
* What would a new developer find confusing after this change?

Remove or simplify anything that produces an unnecessary "because it used to..." explanation.
