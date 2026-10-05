---
name: one-shot-deploy
description: >-
  End-to-end fix-and-ship for trivial DrawExact changes (dxact-draw +
  dxact-wasm): edit, validate, commit on the paired feature branch, then
  production `make deploy` with an agent-composed message. Use only when the
  prompt contains the phrase "one shot deploy" (e.g. "use the one shot deploy
  skill"); never infer it from other talk of shipping or deploying.
---

# One-shot deploy (DrawExact)

## Rationale

Small, eyeball-verifiable changes do not justify a review round-trip. The agent carries the change from edit to production; the user steps in only to agree the change up front and to check the live result.

Safety comes from three layers, each catching what the next cannot:

1. **Agent validation before commit**: tests, build, lints. Catches compile and behaviour breakage while it is still cheap to fix on the feature branch.
2. **Deploy gates** (`dxact-wasm/scripts/deploy.py`): fail closed on dirty trees, `main`, or mismatched branch names; re-run `allnative`, `exportwasm`, `npm test` on squashed `main` before draw is pushed.
3. **User check of the live app**: the agent cannot see the deployed UI.

The deploy script is the authority. When it refuses, the refusal is information to report, not an obstacle to route around.

## Scope

Trivial means: small, localised, behaviour obvious from the diff, verifiable by the user in a minute. Copy, titles, styling, a one-branch logic fix, stale comments.

Not trivial: data/format changes, Drive or auth flows, WASM↔JS interface changes, anything needing a design choice the user has not made. If the change grows past trivial mid-task, stop and say so before committing.

## Preconditions

The user has already:

- Created and checked out the same feature branch in both `dxact-wasm` and `dxact-draw` (sibling repos).
- Agreed what the change is. If the request is a symptom rather than a change, diagnose first, propose, and get the choice before editing.

## Deploy message

The agent composes it. It becomes the squash title on both `main`s and Vercel's deployment label, so it describes the user-visible effect, not the mechanism. When there is none (a rename, refactor, comment or docs tidy), name the change plainly in developer terms instead, e.g. `rename TargetElement to Target`. One line, lowercase, no trailing period, roughly 60 characters at most. Match the tone of recent `git log --oneline` titles on dxact-draw `main`. Example: `fix newbie examples dialogue header`.

## Recipe

1. **Preflight**. In both repos: `git branch --show-current` matches and is not `main`. `git status --short` must be empty, with one exception: if dxact-wasm `docs/log.txt` is the only dirty path, run `git stash push -m one-shot-deploy -- docs/log.txt` there. Any other dirty path: stop and report.
2. **Edit**. Apply the relevant coding skills. Update comments and docs that describe the old behaviour; reuse existing helpers before adding new ones.
3. **Validate**, for each repo touched:
   - dxact-draw: `npm test`, `npm run build`, lints on edited files.
   - dxact-wasm: `make allnative`. Run it before committing: `go generate` / `go mod tidy` may dirty the tree, and deploy refuses a dirty tree.
   - Confirm `git status --short` shows only intended files (build output such as `dist/` must stay ignored).
4. **Commit** on the feature branch, only in repos with changes. One-line message in the repo's existing style. Feature commits are squashed away; the deploy message replaces them on `main`.
5. **Dry run**, from `dxact-wasm`: `make deploy MSG='<message>' DRY_RUN=1`. Gates run for real; no mutations.
6. **Deploy**, from `dxact-wasm`: `make deploy MSG='<message>'`. Allow several minutes. Success ends with `deploy: ok`.
7. **Verify** in both repos: on `main`, clean, `HEAD` equals `origin/main`. dxact-draw tip carries the message. A repo with no changes gets no new commit; that is expected.
8. **Restore log**. If preflight stashed `docs/log.txt`, run `git stash pop` in dxact-wasm (now on `main`).
9. **Report** (see below).

## On failure

Stop at the first failure. Do not retry with variations.

- Before deploy: fix on the feature branch, re-validate, amend or add a commit, restart from the dry run.
- During deploy: do not attempt recovery. Prod pushes wasm `main` before draw `main`, so a mid-run failure can leave repos on `main` with local squash commits or a pushed wasm without its draw counterpart. Report the failing step, its stderr, and per repo: branch, `git status --short`, `git log --oneline -3`, and whether `HEAD` matches `origin/main`. Leave any `docs/log.txt` stash in place and say so. The user decides recovery.

Never: force-push, `--no-verify`, edit `deploy.py` or the `Makefile` to get through, substitute `deploy-preview`, or commit directly on `main`.

## Report

Lead with the outcome (deployed, or where it stopped). Then:

- The deploy message used.
- The change, in a sentence or two per file group.
- Validation run and results.
- Post-deploy state: both repos now on `main` (the user's feature branch is no longer checked out).
- What the agent did not verify: the Vercel build completing, and the behaviour in a browser, including any state needed to reproduce it (e.g. fresh local storage for newcomer flows).
