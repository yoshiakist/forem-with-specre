---
id: "01KJ6EHXR03NS5G0NZKDKT0CA0"
name: "system_loads_billboard_asynchronously"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/javascript/packs/billboard.js`
- `app/javascript/packs/billboardAfterRenderActions.js`
- `app/javascript/utilities/billboardInteractivity.jsx`
- `app/assets/javascripts/initializers/initializeBillboardVisibility.js`
- `app/javascript/__tests__/billboard.test.js` (Test)
- `app/javascript/utilities/__tests__/billboardInteractivity.test.js` (Test)

## Functional Overview

On page load, the system finds all billboard placeholder elements (identified by CSS classes such as `.js-bb-c`, `.js-billboard-container`, and related variants), then fetches each one's content asynchronously from the URL stored in the element's `data-async-url` attribute. Before fetching, the system appends the user's cookie consent status from localStorage and, when the URL carries a `bb_test_placement_area` parameter, forwards the full query string to enable test-mode placement. The `post_fixed_bottom` placement is suppressed for digest-context, internal-navigation, and native-app visits. After injecting the fetched HTML, the system re-executes any inline scripts in the response, applies delayed-display behavior for specially marked billboards, hides any billboard whose dismissal SKU was previously stored in localStorage, sets up a read-more toggle for long billboard bodies, establishes click and impression tracking via `IntersectionObserver` and POSTs to `/bb_tabulations`, initializes sponsorship dropdown interactivity, and attaches a `MutationObserver` to each billboard element to remove any unauthorized attribute injections.

## Design Intent

Billboards are loaded after the initial page render to avoid blocking the critical rendering path. Inline scripts embedded in billboard HTML cannot be executed by simply setting `innerHTML`, so the system clones and re-inserts each `<script>` element to force browser execution. The `MutationObserver` guard exists to prevent third-party ad content from injecting unexpected attributes that could alter page behavior or styling. Impression tracking is deferred by 200 ms and gated on a 25 % visibility threshold via `IntersectionObserver` to reduce false positives from rapid scrolling.

## Key Members

- `data-async-url` — attribute on each placeholder element that provides the fetch endpoint for billboard content
- `data-dismissal-sku` — attribute on a rendered billboard used to identify previously dismissed placements; matched against `dismissal_skus_triggered` in localStorage
- `data-special="delayed"` — attribute that causes the billboard container to be hidden initially and revealed after a 10-second timer
- `cookie_status` in localStorage — when set to `"allowed"`, appends `cookies_allowed=true` to every fetch URL
- `dismissal_skus_triggered` in localStorage — JSON array of SKUs the user has dismissed; used both at load time (to suppress the billboard) and at close time (to record the dismissal)

## Scenarios

### Standard asynchronous load

1. The page contains one or more billboard placeholder elements with `data-async-url` set.
2. `getBillboard()` is called; it collects all matching placeholder elements.
3. For each placeholder, the system reads the cookie consent status from localStorage and appends `cookies_allowed=true` to the URL when consent is granted.
4. The system fetches the URL and injects the HTML response into the placeholder.
5. Inline scripts in the response are cloned and re-inserted so the browser executes them.
6. Impression and click tracking are wired up, and the index is regenerated.

### Test-placement mode

1. The page URL contains the `bb_test_placement_area` query parameter.
2. For each billboard placeholder, the system appends the full query string from the current URL to the `data-async-url` before fetching.
3. The server receives the test parameter and can return the appropriate test content.

### Suppressed post_fixed_bottom placement

1. The page is loaded in a digest-email context (URL contains `context=digest`), via internal navigation (`data-internal-nav="true"`), or inside a native Forem app (user-agent includes `"Forem"`).
2. Any billboard placeholder whose fetch URL contains `post_fixed_bottom` is skipped entirely; no fetch is made and the element remains empty.

### Previously dismissed billboard is hidden

1. The user previously dismissed a billboard with a specific SKU; that SKU is stored in the `dismissal_skus_triggered` array in localStorage.
2. After the billboard HTML is injected, the system reads the `data-dismissal-sku` attribute from the rendered element.
3. If the SKU is present in the localStorage array, the placeholder's display is set to `none` and its content is cleared.

### Billboard dismissal via close button

1. A rendered billboard contains a close button (id prefixed with `sponsorship-close-trigger-`).
2. `setupBillboardInteractivity()` attaches a click listener to the button.
3. When the user clicks the close button (or clicks anywhere outside a popover billboard), the billboard's display is set to `none` and the SKU is appended to `dismissal_skus_triggered` in localStorage.

## Failures / Exceptions

- Network errors (`NetworkError`) during billboard fetch are swallowed silently; no user-facing message is shown and Honeybadger is not notified.
- All other fetch errors are reported to Honeybadger via `Honeybadger.notify(error)`.
- Broken images inside fetched billboard HTML have their `onerror` handler set to `display: none` so a broken image icon is never shown.
- Malformed JSON in `dismissal_skus_triggered` or `last_interacted_billboard` in localStorage is caught and ignored, allowing normal execution to continue.
