---
name: http-handler-dependency-injection
description: >
	Use when generating or modifying Go HTTP handlers, serverless 
	HTTP entrypoints, or Google Cloud Functions.
---


## Invariant

All request logic lives on `Application` methods, never in top-level 
HTTP handlers.

## Rules

- Model external systems as interfaces.
- Aggregate them in `Dependencies`.
- Start `Dependencies` empty and add fields only when required.
- Define `Application` as the owner of request handling logic.
- Construct `Application` with explicit `Dependencies`.
- Top-level HTTP handlers are composition roots only:
  1. construct production `Dependencies`
  2. construct `Application`
  3. delegate immediately to an `Application` method

## Avoid

- request logic in top-level HTTP handlers
- direct external system access from top-level HTTP handlers
- dependency construction inside `Application` methods
- default `Dependencies`, default `Application`, globals, or implicit singletons

