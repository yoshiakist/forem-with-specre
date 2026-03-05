---
id: "01KJ16TGR3DPN82GRT9N6DR7BQ"
name: "moderator_can_flag_user"
status: "draft"
---

## Related Files

- `app/javascript/packs/toggleUserFlagModal.js`
- `app/views/moderations/modals/_flag_user_modal.html.erb` (Template)
- `app/views/moderations/modals/_unflag_user_modal.html.erb` (Template)

## Functional Overview

A moderator viewing an article can open a modal dialog to flag or unflag the article's author. When flagging, the moderator must confirm their intent by selecting a radio button before submitting; the action posts a `vomit` category reaction against the author's `User` record via `POST /reactions`. On success, the modal closes and the toggle button in the moderations panel updates its label and styling to reflect the new state (flagged or unflagged). The same button, now showing the inverse action, is immediately available for the moderator to reverse the decision without a page reload.

## Design Intent

Modal content is extracted from hidden DOM elements on first use and cached in a module-level `Map` to avoid duplicate HTML IDs in the page. The Preact-based modal helper (`showWindowModal`) clones content into the modal overlay, so removing the original hidden element prevents ID conflicts with form controls and ARIA attributes.

## Key Members

- `reactableType`: always `"User"` — the type of entity being reacted to
- `category`: always `"vomit"` — the reaction category that signals a flag
- `reactableId`: the numeric ID of the article author being flagged/unflagged
- `modalContents` (Map): module-level cache of extracted modal HTML keyed by CSS selector

## Scenarios

### Moderator opens the flag dialog

1. The moderator clicks the "Flag `<username>`" button in the moderations panel.
2. The button carries `data-modal-title`, `data-modal-size`, and `data-modal-content-selector` attributes that identify which modal template to show.
3. `toggleFlagUserModal` intercepts the click, retrieves the cached (or freshly extracted) HTML from the `#flag-user-modal-content` hidden element, and opens the window modal with `addModalListeners` registered as the `onOpen` callback.
4. The modal renders a confirmation radio button and a "Confirm Flag" button, along with a link to report other inappropriate conduct.

### Moderator confirms the flag action

1. The moderator selects the radio button ("Make all posts by `<username>` less visible").
2. The moderator clicks "Confirm Flag".
3. The `confirm-flag-user-action` click listener verifies the radio is checked, then calls `flagUser` with `category: "vomit"`, `reactableType: "User"`, and the author's user ID.
4. A `POST /reactions` request is sent with the payload.
5. On a successful `create` result, a snackbar message "All posts by this author will be less visible." is shown and the toggle button in the moderations panel is relabelled to "Unflag `<username>`" with the `c-btn--destructive` class removed.
6. The modal closes.

### Moderator confirms the unflag action

1. The moderator clicks the "Unflag `<username>`" button (previously toggled after a flag).
2. The modal opens showing the `#unflag-user-modal-content` template, which informs the moderator that unflagging will restore default post visibility.
3. The moderator clicks "Confirm Unflag" — no radio selection is required.
4. `flagUser` is called with the same `category` and `reactableType`, sending a `POST /reactions` request.
5. On a successful `destroy` result, a snackbar message "You have unflagged this author successfully." is shown and the toggle button reverts to "Flag `<username>`" with `c-btn--destructive` added back.
6. The modal closes.

### Moderator clicks flag without selecting the radio

1. The moderator opens the flag dialog but does not select the radio button.
2. The moderator clicks "Confirm Flag".
3. The listener detects the unchecked radio and displays the inline error message "You must check the radio button first." in the `#unselected-radio-error` element; no network request is made.

### Moderator clicks the report link

1. Inside the flag dialog, the moderator clicks "Report other inappropriate conduct".
2. The page navigates the parent window to `/report-abuse?url=<article_url>`, closing the modal implicitly via navigation.

## Failures / Exceptions

- If the `POST /reactions` request throws a network error, the caught error is displayed in a snackbar notification and the modal is still closed.
- If the server returns a result other than `"create"` or `"destroy"`, a snackbar shows the raw JSON response so the moderator can see the unexpected outcome.
