---
id: "01KJ1X6T9VWS64SM9K5V94FGEH"
name: "user_can_follow_or_unfollow_a_tag"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/javascript/packs/tagFollows.jsx`
- `app/javascript/tags/TagButtonContainer.jsx`
- `app/javascript/leftSidebar/TagsFollowed.jsx`
- `app/javascript/leftSidebar/__tests__/TagsFollowed.test.jsx` (Test)

## Functional Overview

When a logged-in user visits a page listing tags, each tag card is enhanced with interactive Follow and Hide buttons rendered by the `Tag` component. Clicking "Follow" toggles the follow state for the tag via a POST to `/follows`, and the button label and style update immediately on success along with a snackbar confirmation. Clicking "Hide" similarly marks the tag as hidden (which also removes the Follow button) or unhides it. Tags the user follows with a non-negative point value appear as navigation links in the left sidebar via the `TagsFollowed` component. For logged-out users, clicking any follow or hide button triggers the login modal instead of submitting a request.

## Design Intent

Follow and hide state is encoded in a single `points` field: a non-negative value means followed, a negative value means hidden. This lets the sidebar filter to positive-point tags with a single comparison and avoids maintaining separate boolean flags on the client side.

## Key Members

- `following: boolean` — local state tracking whether the current user follows the tag; derived from whether the tag's `points` value is >= 0
- `hidden: boolean` — local state tracking whether the tag is hidden; derived from whether `points` < 0
- `explicit_points` — sent to `/follows` as `1` for follow/unhide and `-1` for hide
- `verb` — sent to `/follows` as `"follow"` or `"unfollow"` based on the updated follow state

## Scenarios

### Authenticated user follows a tag

1. The page loads and the user's followed tag data is retrieved from their session.
2. Each tag card on the page is rendered with a `Tag` component showing either a "Follow" or "Following" button based on current follow state.
3. The user clicks the "Follow" button on a tag they are not yet following.
4. A POST request is sent to `/follows` with `followable_type: 'Tag'`, the tag's id, `verb: 'follow'`, and `explicit_points: 1`.
5. On success, the button label changes to "Following", the button style updates to outlined, and a snackbar message confirms the action. The browser store cache is cleared.

### Authenticated user unfollows a tag

1. The user clicks the "Following" button on a tag they currently follow.
2. A POST request is sent to `/follows` with `verb: 'unfollow'` and `explicit_points: 1`.
3. On success, the button label reverts to "Follow", the style updates, a snackbar confirms the unfollow, and the cache is cleared.

### Authenticated user hides a tag

1. The user clicks the "Hide" button on a tag card.
2. A POST request is sent to `/follows` with `explicit_points: -1` and `verb: 'follow'`.
3. On success, the Follow button is removed from the card, the Hide button label changes to "Unhide" and adopts a destructive style, and a snackbar confirms the hide. The cache is cleared.

### Authenticated user unhides a tag

1. The user clicks the "Unhide" button on a previously hidden tag.
2. A POST request is sent to `/follows` with `explicit_points: 1` and `verb: 'unfollow'`.
3. On success, the Follow button reappears, the button label reverts to "Hide", and a snackbar confirms the action.

### Logged-out user attempts to follow a tag

1. The page detects the user is logged out via the `data-user-status` attribute.
2. A click listener is attached to the page content area.
3. When the user clicks a follow or hide button, `showLoginModal` is called with tracking data (`referring_source: 'tag'` and the appropriate `trigger` value), prompting login rather than submitting any request.

### Sidebar displays followed tags

1. The `TagsFollowed` component receives the user's list of followed tags as props.
2. Only tags with a `points` value >= 0 are rendered as clickable links navigating to `/t/<name>`.
3. Clicking a tag link triggers an Ahoy analytics event (`Tag sidebar click`) with the link's href.
4. If no tags are passed or all have negative points, the component renders nothing.

## Failures / Exceptions

- If the POST to `/follows` returns a non-OK response, a snackbar displays "An error has occurred." with a close button; local state is not updated.
- If the `TagButtonContainer` module fails to load dynamically, an error is logged to the console and no tag buttons are rendered.
- If the user data or CSRF token cannot be retrieved on page load, an error is logged to the console.
