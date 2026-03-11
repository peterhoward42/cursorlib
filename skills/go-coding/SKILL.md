---
name: go-coding
description: Mandatory rules when generating or editing go source code.
---

## When to apply these rules

- When generating or modifying Go source code.

## init-function-disallowed rule

- You must not use the init() function to initialise any package.
- Rationale:
	- Because a package init() function is often fragile because it gets
	  called implicitly by both production code and test code.
	  Particularly when it requires resources or services only available in 
	  the production environment.
	- An example of the problem being targeted is to initialise an 
	  API that requires network access to authenticate.
