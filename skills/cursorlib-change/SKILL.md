---
name: cursorlib-change
description: >-
  Author a new or changed Cursor skill or rule in the cursorlib master repo,
  then, on explicit go-ahead, commit, push, and install it via the DrawExact
  `install-cursorlib` make targets. Use only when the prompt contains the
  phrase "cursorlib change"; never infer it from other talk of skills or rules.
---

# Cursorlib change

## Model

- **Master**: `~/repos/cursorlib` (GitHub `peterhoward42/cursorlib`), `main` only, no PRs. Skills in `skills/<name>/SKILL.md`, rules in `rules/*.mdc`, index in `README.md`.
- **Installed skills**: `~/.cursor/skills`, global. Installing from any project updates every project.
- **Installed rules**: `<project>/.cursor/rules`, per project and gitignored. Installed into `~/repos/dxact/dxact-wasm` and `~/repos/dxact/dxact-draw`, both by the `dxact-wasm` Makefile. `dxact-draw` has no Makefile, and `~/repos/dxact` itself holds no Cursor files.
- The install targets `rm -rf` their destination before copying. Edits anywhere but cursorlib are lost on the next install, so cursorlib is the only place to edit.

## Phase 1: Preflight

Before any edit:

1. Run `git -C ~/repos/cursorlib status --short`. Every entry must belong to a skill folder or rule file that the prompt names, or be `README.md`. Then run `git -C ~/repos/cursorlib pull --ff-only`.
2. Drift check; each must report differences only for the skills or rules the prompt names:
   - `diff -rq -x .DS_Store ~/repos/cursorlib/skills ~/.cursor/skills`
   - `diff -rq -x .DS_Store ~/repos/cursorlib/rules ~/repos/dxact/dxact-wasm/.cursor/rules`
   - `diff -rq -x .DS_Store ~/repos/cursorlib/rules ~/repos/dxact/dxact-draw/.cursor/rules`

These allowances exist because a change is sometimes drafted in cursorlib during an ordinary chat, before this skill is invoked. Such a draft shows up as uncommitted work, and as a difference from the installed copy, for exactly the skills or rules it touches, and this skill adopts it as its own work in progress. Report which uncommitted changes were adopted.

On any other failure, stop and report. That includes uncommitted changes or differences outside the named skills and rules, and a pull that refuses because of local changes. Drift means an installed copy was edited or the install is stale; the user decides whether to fold it into cursorlib or discard it.

## Phase 2: Authoring

Collaborative and iterative; nothing is committed in this phase.

- Edit in place in cursorlib. Follow `create-skill` for structure and the `markdown-guidelines` rule for prose.
- New skill: folder name equals frontmatter `name`. Trigger by explicit phrase when the skill has side effects.
- Keep `README.md` in step: add or update the "Skill index" entry, and "Composing skills" when the skill depends on or pairs with others.
- Rename or removal: follow `removing-stuff-policy`; grep cursorlib for references to the old name and update them.
- When the change looks complete, show `git -C ~/repos/cursorlib status --short` and the diff, then wait.

## Phase 3: Publish

Only after an explicit go-ahead such as "publish it". Agreement that the content is right is not a go-ahead. Stop at the first failure.

1. **Commit** in cursorlib, staging only the intended paths. One-line message matching `git log --oneline` tone, e.g. `Add one-shot-deploy skill for trivial DrawExact changes`, `Soften markdown rule`.
2. **Sync**: `git pull --rebase`, then `git push`. On a rebase conflict, `git rebase --abort` and report.
3. **Install**: `make -C ~/repos/dxact/dxact-wasm install-cursorlib`. This installs skills globally and rules into both wasm and draw.
4. **Verify**: the Phase 1 drift check prints nothing, and `git -C ~/repos/cursorlib status -sb` shows `main...origin/main` with nothing ahead or behind.

Never force-push, commit drafts, or edit the Makefiles to get through.

## Report

Lead with the outcome (published, or where it stopped). Then the commit title and short hash, files changed, and installs run. Note that a new or renamed skill appears in the skill list only in a new chat.
