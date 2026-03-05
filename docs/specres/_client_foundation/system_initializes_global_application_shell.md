---
id: "01KJXXHCPNS5J9D2D3NGMGWSSP"
name: "system_initializes_global_application_shell"
status: "draft"
---

## Related Files

- `app/javascript/packs/application.jsx`
- `app/javascript/packs/baseInitializers.js`

## Functional Overview

On every page load, the application assembles the global JavaScript shell in two coordinated entry-point packs. `application.jsx` establishes the `window.Forem` namespace, polyfills `Document.prototype.ready`, wires up top navigation, lazy-loads route-specific modules (dashboard sort, video playback), registers InstantClick page-transition handlers, tracks account-creation click events, and defers non-critical setup — such as scroll-restoration and search-script injection — until the DOM is fully ready. `baseInitializers.js` complements this by running a fixed set of UI micro-initializers (comment dates, comment preview, time display, notification badge, date helpers, GIF-to-video replacement, settings) at startup and again on each InstantClick navigation change, and exposes two alert-modal helpers onto the global `window` object for use by server-rendered markup.

## Design Intent

Splitting initialization across two packs allows `baseInitializers.js` to be included in pages that do not need the full Forem namespace or navigation wiring, while `application.jsx` is reserved for pages that render the full top-navigation shell. The lazy `import()` calls for `preact`, `CommentTextArea`, dashboard sort, and video playback keep the initial bundle small and only pay the parse cost for those modules when they are actually needed. Caching the preact import promise on `window.Forem.preactImport` prevents redundant dynamic imports across multiple callers.

## Key Members

- `window.Forem` — global namespace that exposes `audioInitialized`, `getPreactImport()`, `getEnhancedCommentTextAreaImports()`, `initializeEnhancedCommentTextArea()`, `showModal`, `closeModal`, and `Runtime`
- `Document.prototype.ready` — promise that resolves when `DOMContentLoaded` fires (or immediately if the document is already interactive)
- `window.showUserAlertModal` / `window.showModalAfterError` — alert-modal helpers exposed globally for server-rendered HTML

## Scenarios

### Application shell boots on initial page load

1. The browser parses `application.jsx` before the DOM is fully loaded.
2. `Document.prototype.ready` is attached as a promise; if the document is already past the loading state the promise resolves immediately, otherwise it waits for `DOMContentLoaded`.
3. `window.Forem` is created with audio state, lazy-loaded module accessors, modal helpers, and the current runtime context.
4. The current runtime context is written to `document.body.dataset.runtime`.
5. `initializeNav()` runs synchronously to set the active icon link and wire up mobile menu triggers.
6. If a member menu element is present, `initializeMemberMenu` is called to enable it.
7. After `waitOnBaseData()` resolves, an InstantClick `change` listener is registered to re-initialize navigation on subsequent SPA navigations; if the context is `ForemWebView`, the mobile Forem module is loaded and a user-session broadcast is initiated.

### Route-specific modules are loaded lazily on dashboard and video pages

1. On initial load, if the URL path starts with `/dashboard`, the dashboard-sort initializer is imported and executed.
2. If a `#video-player-source` element is present, the video playback initializer is imported and executed.
3. On each InstantClick `change` event the same conditions are re-evaluated and the relevant modules re-imported as needed.

### Deferred DOM-ready setup runs after DOMContentLoaded

1. Once `document.ready` resolves, scroll restoration is switched to `manual` via `setTimeout` to allow the browser to finish its default scroll handling first.
2. A click listener is attached to the hamburger trigger that fetches navigation links from `/async_info/navigation_links` and injects them into the placeholder container (only if the container is currently empty).
3. If a `meta[name="search-script"]` element is present, a one-time `mouseenter` listener on the search input lazily appends the referenced script to `<head>`.

### Base UI micro-initializers run on every page

1. `baseInitializers.js` is executed; it calls comment-date, comment-preview, settings, notifications, time-fixer, date-helpers, and GIF-video initializers in sequence.
2. Two alert-modal functions are attached to the global `window` object for use by inline server-rendered handlers.
3. On each InstantClick `change` event the comment-date, comment-preview, settings, notifications, and GIF-video initializers are re-run to reinstate UI behaviors on the newly rendered page content.

### Creator-settings Stimulus controller is registered on the admin page

1. When the URL is exactly `/admin/creator_settings/new`, `loadCreatorSettings()` is called.
2. The `LogoUploadController` and the Stimulus `Application` class are imported in parallel.
3. A Stimulus application instance is started and `LogoUploadController` is registered under the `logo-upload` identifier.

## Failures / Exceptions

- If `waitOnBaseData()` rejects (e.g., a network or runtime error), the error is forwarded to `Honeybadger.notify` so it is captured in the error-tracking service without crashing the page.
- If `loadCreatorSettings()` throws during the dynamic import or controller registration, the error message is sent to `Honeybadger.notify` with a descriptive prefix and the function returns silently.
