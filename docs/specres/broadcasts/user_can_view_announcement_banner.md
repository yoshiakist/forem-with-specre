---
id: "01KJ6DVV4TY3RHBN045KGH5ZXY"
name: "user_can_view_announcement_banner"
status: "draft"
---

## Related Files

- `app/assets/javascripts/initializers/initializeBroadcast.js`
- `app/models/broadcast.rb`
- `app/helpers/broadcasts_helper.rb`

## Functional Overview

When a site administrator creates an active `Announcement` broadcast, a styled banner is injected into the page for all users who have not previously dismissed it. The broadcast's HTML content and optional banner style are embedded in the page's `<body>` dataset and parsed client-side on initialization. The banner renders with a close button; clicking it stores the broadcast title as a key in `localStorage` and removes the element from the DOM, preventing it from re-appearing on subsequent page loads. The banner is suppressed in iframes, on `/connect` and `/new` routes, and for users who have opted out of announcements.

## Design Intent

Broadcast data is serialized into `document.body.dataset` server-side so the client needs no additional API call to render the banner. Using `localStorage` to track dismissal keeps the state client-local, avoiding a round-trip on every page load and not requiring a user session.

## Key Members

- `banner_style` — one of `default`, `brand`, `success`, `warning`, or `error`; controls the CSS class applied to the banner element
- `camelizedBroadcastKey(title)` — derives the `localStorage` key from the broadcast title to track per-broadcast dismissal state
- `display_announcements` — user preference flag; when `false` the banner is never rendered for that user

## Scenarios

### User views the banner for the first time

1. An active `Announcement` broadcast exists and its serialized data is embedded in the page body.
2. The page initializes and `initializeBroadcast` runs outside of an iframe and not on a suppressed route.
3. The user has not previously dismissed this broadcast and has `display_announcements` enabled.
4. The banner HTML and optional style class are inserted into the `active-broadcast` element.
5. A close button is appended and the element receives the `broadcast-visible` class, making it visible.

### User dismisses the banner

1. The announcement banner is visible on the page.
2. The user clicks the close button.
3. A key derived from the broadcast title is written to `localStorage` with value `true`.
4. The `active-broadcast` element is removed from the DOM.
5. On all subsequent page loads, `initializeBroadcast` reads the `localStorage` key and skips rendering.

### Banner is suppressed on excluded routes

1. The user navigates to `/connect` or `/new`, or the page is loaded inside an iframe.
2. `initializeBroadcast` detects the condition and, if the `active-broadcast` element exists, removes the `broadcast-visible` class.
3. No banner content is injected.

### User has opted out of announcements

1. An active broadcast exists but the authenticated user's `display_announcements` preference is `false`.
2. `initializeBroadcast` reads the user data and returns early without rendering the banner.

## Failures / Exceptions

- If no broadcast data is present in the page body dataset, `broadcastData()` returns `null` and initialization exits silently.
- Only one active `Announcement` broadcast is permitted at a time; the `single_active_announcement_broadcast` model validation enforces this constraint.
