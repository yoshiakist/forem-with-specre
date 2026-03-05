---
id: "01KJXY52M1WTZV87HQC7P452C0"
name: "system_displays_runtime_context_banner"
status: "draft"
---

## Related Files

- `app/javascript/packs/runtimeBanner.jsx`

## Functional Overview

When the page is ready, the system mounts the `RuntimeBanner` Preact component into the `#runtime-banner-container` DOM element. Initialization is deferred until base application data is available via `waitOnBaseData`, preventing a race condition that can occur during initial page load or sign-out. Once mounted, the banner is also re-rendered on every InstantClick page change so it stays current across client-side navigation. Errors during initialization are forwarded to Honeybadger.

## Design Intent

The banner is deferred behind `waitOnBaseData` — following the same pattern used by the listings and Chat packs — because it appears on every page including the main feed, and the base data it depends on may not yet be present during the first render or after a sign-out clears the cache. Hooking into the InstantClick `change` event ensures the banner re-initializes after each soft navigation without requiring a full page reload.

## Scenarios

### Page loads successfully with the container present

1. The browser parses the page and the webpack entry point runs.
2. `waitOnBaseData` resolves once the base application data is available.
3. The system calls `loadElement`, which finds `#runtime-banner-container` in the DOM.
4. The `RuntimeBanner` component is rendered into the container.
5. The banner becomes visible to the user.

### InstantClick page change after initial load

1. The user navigates to a new page via InstantClick (client-side navigation).
2. InstantClick fires the `change` event.
3. The system calls `loadElement` again.
4. If `#runtime-banner-container` is present in the updated DOM, `RuntimeBanner` is re-rendered into it.

### Container element is absent from the DOM

1. `waitOnBaseData` resolves.
2. `loadElement` runs but `document.getElementById('runtime-banner-container')` returns `null`.
3. No rendering occurs; the function exits silently.

## Failures / Exceptions

- If `waitOnBaseData` rejects (e.g., a network error or timeout before base data arrives), the caught error is forwarded to `Honeybadger.notify` for monitoring, and the banner is not mounted.
