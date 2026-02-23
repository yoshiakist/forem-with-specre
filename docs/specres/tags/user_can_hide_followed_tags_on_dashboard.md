---
id: "01KJ41J4101Y3KSMXR9VEHN9ZY"
name: "user_can_hide_followed_tags_on_dashboard"
status: "draft"
---

## Related Files

- `app/javascript/packs/dashboardTags.js`
- `app/views/dashboards/_tags.html.erb` (Template)
- `app/views/dashboards/hidden_tags.html.erb` (Template)

## Functional Overview

On the dashboard's followed-tags page, a user can hide any followed tag by clicking the "Hide" option from that tag's overflow dropdown. Hiding a tag sends a follow request to the `/follows` API endpoint with `explicit_points: -1`, which deprioritises the tag in the feed. On success, the tag card is immediately removed from the followed-tags list, the followed-tags navigation counter is decremented, and the hidden-tags navigation counter is incremented. A separate hidden-tags page lists all such suppressed tags and allows the user to unhide them, which removes the follow record entirely and removes the card from that page.

## Design Intent

Hiding a tag does not unfollow it outright; instead it sets `explicit_points` to `-1` to signal a negative preference. This preserves the follow relationship so the system can distinguish "actively ignored" tags from tags the user never followed, enabling feed-ranking logic to suppress hidden content rather than simply omitting it.

## Key Members

- `explicit_points: -1` — the numeric signal sent in the POST body that marks a follow as hidden rather than a normal follow
- `.js-hidden-tags-link .c-indicator` — the DOM element whose text count is updated to reflect the number of hidden tags in the sidebar navigation
- `.crayons-link--current .c-indicator` — the DOM element whose text count is decremented when a tag card is removed from the current view

## Scenarios

### User hides a followed tag

1. On the followed-tags dashboard page, the user clicks the overflow (options) button on a tag card, revealing a dropdown with a "Hide" option.
2. The user clicks the "Hide" button.
3. The browser posts to `/follows` with `followable_type: 'Tag'`, the tag's ID, `verb: 'follow'`, and `explicit_points: -1`.
4. On a successful response, the tag card is removed from the page, the followed-tags navigation count decreases by one, and the hidden-tags navigation count increases by one.

### User views hidden tags

1. The user navigates to the hidden-tags dashboard page.
2. If any tags are hidden, their cards are displayed using the shared `_tags` partial rendered in `"hidden"` mode, showing an "Unhide" button on each card instead of the following/options controls.
3. If no tags are hidden, an empty-state message is shown with a link to browse all tags.

### User unhides a tag from the hidden-tags page

1. On the hidden-tags dashboard page, the user clicks the "Unhide" button on a tag card.
2. The browser posts to `/follows` with `followable_type: 'Tag'`, the tag's ID, and `verb: 'unfollow'`.
3. On a successful response, the tag card is removed from the hidden-tags page and the hidden-tags navigation count decreases by one.

### Dropdown is initialised for each tag card

1. When the followed-tags page loads, each tag card's overflow dropdown is initialised by associating its trigger button (`options-dropdown-trigger-<tagId>`) with its content panel (`options-dropdown-<tagId>`).
2. When new tag cards are inserted into the DOM (e.g., via pagination), a `MutationObserver` detects the additions and initialises the dropdown for each newly added card automatically.

## Failures / Exceptions

- If the `/follows` request returns a non-OK HTTP status for a hide, unfollow, or unhide action, `showModalAfterError` is called with a contextual description of the failed action, informing the user that the update could not be completed.
- Network-level errors (fetch rejections) for hide and unfollow actions are logged to the console; the tag card is not removed from the page in these cases.
- The `MutationObserver` skips added DOM nodes that have no child nodes (such as bare text nodes) to avoid errors when accessing dataset properties on non-element nodes.
- The `MutationObserver` is disconnected on `InstantClick` page changes and on `beforeunload` to prevent stale listeners from operating after navigation.
