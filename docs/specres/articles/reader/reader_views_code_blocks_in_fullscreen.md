---
id: "01KJCKQZYF0GEXFX0H120R12QN"
name: "reader_views_code_blocks_in_fullscreen"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/javascript/utilities/codeFullscreenModeSwitcher.js`
- `app/javascript/packs/fullScreenModeControl.js`
- `app/javascript/packs/articlePage.jsx`
- `app/views/articles/show.html.erb`
- `app/javascript/utilities/__tests__/codeFullscreenModeSwitcher.test.js` (Test)

## Functional Overview

When an article contains syntax-highlighted code blocks, each block rendered with the `.js-code-highlight` class receives a fullscreen toggle button (`.js-fullscreen-code-action`). Clicking the button clones the code block into a full-viewport overlay container (`.js-fullscreen-code`), sets the `is-open` and `is-fullscreen` CSS classes, locks body scroll, saves the current scroll position, and registers listeners for both the Escape key and the browser `popstate` event so the reader can exit fullscreen. Exiting — via Escape key, clicking the toggle button again, or browser back navigation — reverses all of those steps: the overlay is cleared, scroll lock is removed, the page scrolls back to its saved position, and all event listeners are torn down.

## Design Intent

The fullscreen overlay is CSS-driven (`is-open` / `is-fullscreen` classes) rather than relying on the browser's native Fullscreen API, which gives the team full control over styling and avoids permissions differences across browsers. Cloning the code block into the overlay (rather than moving it) ensures the original article DOM remains intact when fullscreen is closed. Browser history push is avoided; instead, the existing `popstate` event is listened to so that pressing the browser back button exits fullscreen without navigating away from the article.

## Scenarios

### Reader enters fullscreen mode

1. The article page loads with one or more syntax-highlighted code blocks, each containing a `.js-fullscreen-code-action` toggle button.
2. `articlePage.jsx` (and `fullScreenModeControl.js` via `DOMContentLoaded`) calls `addFullScreenModeControl` on all `.js-fullscreen-code-action` elements, attaching a click listener to each.
3. The reader clicks the toggle button on a code block.
4. The utility saves the current scroll position, locks body scroll (`overflow: hidden`), clones the code block into the `.js-fullscreen-code` overlay container, adds `is-open` to the overlay and `is-fullscreen` to the cloned block, registers the Escape key listener on `document.body`, and registers the `popstate` listener on `window`.
5. The code block is displayed in a full-viewport overlay; the rest of the page is hidden behind it.

### Reader exits fullscreen via Escape key

1. The reader is viewing a code block in fullscreen mode.
2. The reader presses the Escape key.
3. The `keyup` listener on `document.body` detects `event.key === 'Escape'` and calls `fullScreenModeControl`.
4. The overlay's `is-open` class is removed, the cloned code block is removed from the overlay, body scroll is restored, the saved scroll position is restored, and both the `keyup` and `popstate` listeners are removed.
5. The article page returns to its normal layout.

### Reader exits fullscreen by clicking the toggle button again

1. The reader is viewing a code block in fullscreen mode.
2. The reader clicks the `.js-fullscreen-code-action` button visible within the fullscreen overlay.
3. `fullScreenModeControl` is called with the click event.
4. The same teardown sequence runs: overlay closed, cloned block removed, scroll restored, listeners removed.
5. The article page returns to its normal layout.

### Reader exits fullscreen via browser back navigation

1. The reader is viewing a code block in fullscreen mode.
2. The reader activates the browser's back navigation (e.g., presses the Back button or uses a gesture).
3. The `popstate` listener on `window` fires and calls `fullScreenModeControl`.
4. The overlay is closed and all state is restored, keeping the reader on the same article page rather than navigating away.
5. The article page returns to its normal layout.

## Failures / Exceptions

- If no `.js-fullscreen-code` element exists in the DOM when a toggle button is clicked, `fullScreenModeControl` will throw because `fullScreenWindow` will be `undefined`. The template in `show.html.erb` always renders `<div class="fullscreen-code js-fullscreen-code"></div>`, so this should not occur in production.
- If the clicked element is not inside a `.js-code-highlight` ancestor, `codeBlock` is set to `null` and no code content is appended to the overlay. The overlay will still open (and state will be set), but it will display empty.
- Pressing keys other than Escape while in fullscreen mode is ignored by the keyboard listener.
