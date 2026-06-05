---
name: go-linting
description: >-
  Run golangci-lint and fix all reported issues in a Go codebase. Use only when
  the user explicitly asks to lint or fix linter errors.
disable-model-invocation: true
---

## When to apply this skill

- Only when I ask you to explicitly

## The linter command to use

- Use the command line linter golangci-lint using the command line below
- Do not alter the commands default configuration

```
golangci-lint
```

## Fixing the linter errors

- Make changes to the code to fix the linter reported errors
- Repeat the process as necessary until there are no reported errors

