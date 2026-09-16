# Example code review guide produced by this skill


## Preamble

- The code example code review guide starts lower down this page after the
  horizontal rule section delimeter
- This preamble is to give you just enough orientation about the code it is
  reviewing -so you can make sense of it

### Just sufficient orientation

The code is part of a javascript web app for technical drawing that stores 
the drawing files they create on their own Google Drive.  (Drive)

Its architecture for Identity, Authorisation and Access Permissions is 
Google's *Google Identity Services OAuth 2.0 Token Model / Token Client*

For the purposes of this code review you need to know that every Drive related
action seeks a new token from Google's token client, which, when necessary,
invokes Google's popups for Google Sign In and the permission's gate, but then
yields a token that is good for approximately one hour.


## Some shorthand terms the review guide uses:

- gapi = Google API
- 401 = http access denied return code
- DrawExact = name of the product DrawExact
- bearer = Bearer Token
- DriveWrapper = low level single place in code that all Drive operations go through
- developer fake = a developer only switch to fake token expiry for testing
- fake expiry = same
- drive ops = Drive Operations
- runDriveOperation = high level single place that wraps every Drive CRUD
  operation with a token aquirer

---

## Real Generated Code Review Guide Starts here

# Code review: on-demand Drive bearer refresh

Scope: generated code from implementing [`drive-token-expiry-refresh-plan.md`](./drive-token-expiry-refresh-plan.md). Design rationale: [`drive-token-expiry-as-product-feature.md`](./drive-token-expiry-as-product-feature.md).

## Why this changed

Visit-scoped Drive connect reused an in-memory GIS access token without tracking lifetime. After ~1 hour the bearer was dead; the next Drive call got 401 and surfaced as FatalError. The product goal is: refuse known-dead bearers, narrate a DrawExact refresh beat when connected this visit, renew GIS only on Continue, keep 401 as a bounded safety net.

## Conceptual change


Three facts are now distinct in code:

- **Not connected this visit** — connect-on-need owns entry (unchanged product story).
- **Connected, bearer fresh** — reuse; no auth UX.
- **Connected, bearer unusable** — refresh coaching before Drive `fetch`; GIS only after Continue.

Freshness is visit-scoped metadata beside the gapi token, not localStorage. The obtain gate lives in the Drive wrapper so every call site is covered.

## Essence

Record `expires_at` on GIS success → `isDriveBearerUsable()` before send → if connected and unusable, thin refresh helpers (panel + renew) → on 401, clear once and re-enter that path; do not FatalError-as-auth.

---

## Survey order

Read in this order. Open each link; the code carries the detail.

### 1. Lifetime metadata

[`dxact-draw/src/services/driveconnect/bearerMetadata.ts`](../../../dxact-draw/src/services/driveconnect/bearerMetadata.ts)

In-memory `expires_at` (with skew), store/clear paired with the gapi token, usable query, and the developer fake that forces expiry metadata so usable checks fail until renew.

Ask while reading: does clear always clear expiry too? Does the developer fake leave the token string in place while marking expiry past?

### 2. Refresh helpers (mirror of connect-on-need)

[`dxact-draw/src/services/driveconnect/refreshBearer.ts`](../../../dxact-draw/src/services/driveconnect/refreshBearer.ts)

Thin procedural pair: DrawExact ask (`makeSureDriveBearerFresh`) then GIS renew (`renewDriveBearer`). Compare shape to [`connectOnNeed.ts`](../../../dxact-draw/src/services/driveconnect/connectOnNeed.ts) — same closure `dataForChild` pattern, no resume bags.

Ask: when does the ask no-op (usable, or not connected)? Does renew always use `prompt: ""` + visit `login_hint`?

### 3. Refresh panel

[`dxact-draw/src/cpts/driveconnect/RefreshDriveAccess.svelte`](../../../dxact-draw/src/cpts/driveconnect/RefreshDriveAccess.svelte)

Lifetime copy only. Sibling of [`ConnectDrive.svelte`](../../../dxact-draw/src/cpts/driveconnect/ConnectDrive.svelte) — same Continue/Cancel chrome, different story.

Ask: could this copy be mistaken for first-time connect?

### 4. Wrapper obtain path (heart of the change)

[`dxact-draw/src/services/asyncdrivewrapper.ts`](../../../dxact-draw/src/services/asyncdrivewrapper.ts)

All Drive ops enter here. Survey the branch order in `obtainBearerAndRun`:

1. usable → run op
2. connected + unusable → refresh beat → run op
3. not connected → first-grant GIS (existing path)

Then `runDriveOperation` and the one-shot 401 recover (`from401Recover` / `allow401Recover`). Decline rejects without `handleJavaScriptError`.

Ask: can refresh and first-connect UI both appear for one call? Is a second 401 after recover still FatalError-free? Does first-grant still persist expiry via `storeDriveBearer`?

### 5. Developer launcher

[`dxact-draw/src/cpts/dev/ManageState.svelte`](../../../dxact-draw/src/cpts/dev/ManageState.svelte)

Drive (session) section: fake expire-on-next-op. Reached via Developer Tools → Manage state.

fart
Ask: does setting the fake alone call Google or open the refresh panel, or only affect the next usable check?

### 6. Operational docs (if verifying prose matches behaviour)

- [`../dxact-draw/identity-and-auth.md`](../dxact-draw/identity-and-auth.md) — expiry awareness, refresh beat, 401 residual role
- [`../dxact-draw/drive-integration.md`](../dxact-draw/drive-integration.md) — wrapper obtain wording

---

## Suggested smoke while reviewing

Use Developer Tools → Manage state → **Fake Drive bearer expiry on next op**, then Save / list / open: expect refresh panel only when already connected this visit; Cancel leaves drawing usable and Drive gated; not-connected paths should still show Connect Drive only.
