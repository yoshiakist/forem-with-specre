---
id: "01KHYCQP8ZV9CETSKG0HMGF2XP"
name: "user_follows_or_hides_tag"
status: "draft"
---

## Related Files

- app/javascript/tags/TagButtonContainer.jsx

## Functional Overview

The `Tag` Preact component renders Follow and Hide toggle buttons on tag cards. It manages local follow/hidden state and communicates with the server via POST requests to the `/follows` endpoint. State changes are confirmed with snackbar notifications, and the browser store cache is cleared on success to ensure fresh data on subsequent loads.

## Scenarios

### User follows or unfollows a tag

1. When the user clicks the Follow button, the component sends a POST to `/follows` with `followable_type: 'Tag'`, the tag ID, a `follow` or `unfollow` verb, and `explicit_points: 1`.
2. On success, the button label toggles between "Follow" and "Following", and a snackbar confirms the action (e.g., "You have followed javascript.").
3. The browser store cache is cleared to ensure the followed tags list is refreshed.
4. On failure, an error snackbar is displayed.

### User hides or unhides a tag

1. When the user clicks the Hide button, the component sends a POST to `/follows` with `hidden: true` and `explicit_points: -1`.
2. On success, the button label toggles between "Hide" and "Unhide", and a snackbar confirms the action.
3. When a tag is hidden, the Follow button is not rendered (only the Unhide button is visible).
4. When the user unhides a tag, both Follow and Hide buttons become visible again.
5. Hiding a tag also sets `following: true` (the tag enters a "followed but hidden" state with negative points); unhiding sets `following: false`.

### Component renders accessible button labels

1. Each button includes an `aria-label` that describes the action and the tag name (e.g., "Follow tag: javascript").
2. The Follow button includes `aria-pressed` reflecting the current follow state.
