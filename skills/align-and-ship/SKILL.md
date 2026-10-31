---
name: align-and-ship
description: >-
  DrawExact paired-repo workflow (dxact-draw + dxact-wasm): discuss until
  aligned, then on an explicit proceed phrase create throwaway feature
  branches, implement, validate, commit, and production `make deploy`. Use
  only when the prompt starts a session with the align-and-ship workflow
  wording (see skill body); never infer ship from ordinary talk of changes,
  commits, or deploy.
---

# Align and ship (DrawExact)

This skill is a two-phase ritual for changes that usually touch both
`dxact-wasm` and `dxact-draw`. Phase one is discussion until Pete and the
agent share one understanding of what to do. Phase two, after an explicit
proceed phrase, is autonomous: paired throwaway branches, implementation,
validation, matching commits, and production deploy. Pete decides whether
the change is wise to ship this way. The skill does not judge triviality or
refuse on scope grounds.

Safety still comes from three layers, each catching what the next cannot.
Agent validation before commit catches compile and behaviour breakage while
it is cheap to fix on the feature branch. Deploy gates in
`dxact-wasm/scripts/deploy.py` fail closed on dirty trees, `main`, or
mismatched branch names, and re-run `allnative`, `exportwasm`, and
`npm test` on squashed `main` before draw is pushed. Pete checks the live
app, which the agent cannot see. The deploy script is the authority. When
it refuses, the refusal is information to report, not an obstacle to route
around.

This skill replaces `one-shot-deploy`.

## Triggers

Load this skill when the user opens with workflow wording such as:

`Let's work on some changes using the align-and-ship (skill) workflow`

Until the proceed phrase arrives, stay in discussion: clarify intent,
propose options when needed, and reach a shared plan. Do not create
branches, edit product code, commit, or deploy.

Start the ship phase only when a user message **begins with** exactly:

`We are now aligned, so proceed`

Anything after that prefix on the same message may add detail. Do not treat
"looks good", "go ahead", "make it so", "implement that", or agreement that
stops short of this opening as the gate.

## Align phase

Discuss until Pete can send the proceed phrase. Prefer a concrete plan:
what changes, in which repo, and what user-visible or developer-facing
outcome the deploy message should name. If the request is a symptom rather
than a change, diagnose and get the choice before treating the plan as
aligned. Do not start ship work early.

## Ship phase

Run only after the proceed phrase. Do not pause for approval of the diff.

### Deploy message

Compose one line that will be the feature-branch commit message in every
repo that changes, and the `MSG` passed to `make deploy`. It becomes the
squash title on both `main`s and Vercel's deployment label, so describe the
user-visible effect when there is one, not the mechanism. When there is
none (a rename, refactor, comment or docs tidy), name the change plainly in
developer terms instead, for example `rename TargetElement to Target`.
Lowercase, no trailing period, roughly 60 characters at most. Match the
tone of recent `git log --oneline` titles on dxact-draw `main`. Example:
`fix newbie examples dialogue header`.

### Recipe

1. **Branch**. Both repos must be on `main`. From `dxact-wasm`, create a
   paired throwaway branch with an arbitrary available name (it need not
   describe the change), for example
   `make feature-branch NAME='aas-<short-unique>'`. Optional:
   `DRY_RUN=1` first. `feature-branch` already tolerates dirty
   `docs/log.txt` in wasm and `public/main.wasm` in draw. If it refuses
   for any other reason (material dirty paths, not on `main`, behind
   `origin/main`, name taken), stop and report; do not work around the
   gates.

2. **Edit**. Apply the relevant coding skills. Update comments and docs
   that describe the old behaviour; reuse existing helpers before adding
   new ones.

3. **Validate**, for each repo touched:
   - dxact-draw: `npm test`, `npm run build`, lints on edited files.
   - dxact-wasm: `make allnative`. Run it before committing: `go generate`
     / `go mod tidy` may dirty the tree, and deploy refuses a dirty tree.
   - Confirm `git status --short` shows only intended files (build output
     such as `dist/` must stay ignored). Never commit `docs/log.txt` or
     `public/main.wasm`. If draw `public/main.wasm` has been rewritten by
     a local build, `git restore -- public/main.wasm` there; deploy
     rebuilds it from squashed `main`. If wasm `docs/log.txt` is dirty and
     gets in the way of a clean status check, stash it with
     `git stash push -m align-and-ship -- docs/log.txt` and remember to
     pop after deploy.

4. **Commit** on the feature branch, only in repos with changes. Use the
   same deploy message string in each repo. Feature commits are squashed
   away; the deploy message replaces them on `main`.

5. **Dry run**, from `dxact-wasm`: `make deploy MSG='<message>' DRY_RUN=1`.
   Gates run for real; no mutations.

6. **Deploy**, from `dxact-wasm`: `make deploy MSG='<message>'`. Allow
   several minutes. Success ends with `deploy: ok`.

7. **Verify** in both repos: on `main`, clean aside from any restored
   ignorable paths, `HEAD` equals `origin/main`. dxact-draw tip carries
   the message. A repo with no changes gets no new commit; that is
   expected.

8. **Restore log**. If the ship phase stashed `docs/log.txt`, run
   `git stash pop` in dxact-wasm (now on `main`).

9. **Report** (see below).

### On failure

Stop at the first failure. Do not retry with variations.

Before deploy: fix on the feature branch, re-validate, amend or add a
commit, restart from the dry run.

During deploy: do not attempt recovery. Prod pushes wasm `main` before
draw `main`, so a mid-run failure can leave repos on `main` with local
squash commits or a pushed wasm without its draw counterpart. Report the
failing step, its stderr, and per repo: branch, `git status --short`,
`git log --oneline -3`, and whether `HEAD` matches `origin/main`. Leave
any `docs/log.txt` stash in place and say so. Pete decides recovery.

Never: force-push, `--no-verify`, edit `deploy.py` or the `Makefile` to
get through, substitute `deploy-preview`, or commit directly on `main`.

### Report

Lead with the outcome (deployed, or where it stopped). Then:

- The deploy message used.
- The change, in a sentence or two per file group.
- Validation run and results.
- Post-deploy state: both repos now on `main` (the throwaway feature
  branch is no longer checked out).
- What the agent did not verify: the Vercel build completing, and the
  behaviour in a browser, including any state needed to reproduce it
  (for example fresh local storage for newcomer flows).
