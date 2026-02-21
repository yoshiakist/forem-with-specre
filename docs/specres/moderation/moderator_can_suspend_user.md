---
id: "01KJ16YRQGJ8SK83RGN8MJ78V5"
name: "moderator_can_suspend_user"
status: "draft"
---

## Related Files

- `app/javascript/packs/toggleUserSuspensionModal.js`
- `app/views/moderations/modals/_suspend_user_modal.html.erb` (Template)
- `app/views/moderations/modals/_unsuspend_user_modal.html.erb` (Template)

## Functional Overview

When a moderator views an article's moderation panel, they can suspend or unsuspend the article's author via a modal dialog. Clicking the suspend or unsuspend button opens a window modal populated with either the suspend or unsuspend form. The moderator must provide a written reason before submitting. On submission the form sends a PATCH request to `/admin/member_manager/users/:id/user_status` with the new status and the reason note. If the request succeeds, a snackbar notification is shown and the trigger button is toggled to reflect the opposite action; if it fails, an error snackbar is shown instead.

## Design Intent

Modal content is extracted from the DOM on first use and cached in a `Map`, then the original hidden element is removed. This prevents duplicate HTML IDs in the document when the Preact modal helper clones content into the overlay, which would otherwise break `<label for>` and `aria-describedby` associations.

## Key Members

- `btnAction` — string value, either `"suspend"` or `"unsuspend"`, carried as a `data-btn-action` attribute on submit buttons and used to determine the API payload and button toggle direction
- `modalContentSelector` — CSS selector string stored as `data-modal-content-selector` on the trigger button, used to locate the correct hidden modal HTML fragment
- `modalContents` — module-level `Map` that caches extracted modal HTML by selector to avoid repeated DOM queries and duplicate-ID problems

## Scenarios

### Moderator opens the suspend modal

1. The moderator clicks the "Suspend {username}" button in the moderation panel.
2. `toggleSuspendUserModal` is called with the click event.
3. The function reads `modalTitle`, `modalSize`, and `modalContentSelector` from the button's dataset.
4. If this is the first time this selector has been used, `getModalContents` finds the matching hidden element in the parent document, copies its inner HTML, removes the original element from the DOM, and stores the content in `modalContents`.
5. `showWindowModal` is called with the cached HTML, the title, and `activateModalSubmitBtn` as the `onOpen` callback.
6. The modal opens in the parent document and the submit button listener is attached.

### Moderator submits a suspension with a valid reason

1. The moderator types a reason into the textarea inside the modal and clicks the confirm button (`submit-user-suspend-btn`).
2. `checkReason` fires; it reads the reason value from the textarea identified by `data-reason-selector`.
3. Because the reason is non-empty, `suspendOrUnsuspendUser` is called with `btnAction="suspend"`, the user ID, username, and the reason text.
4. The modal is closed immediately, and a PATCH request is sent to `/admin/member_manager/users/:id/user_status` with `user_status: "Suspended"` and `note_for_current_role` set to the reason.
5. On a successful response, a snackbar displays the server's success message.
6. `updateBtnFlow` rewrites the trigger button to read "Unsuspend {username}", assigns it the `unsuspend` action and selector, and adds the `c-btn--destructive` class is removed (since unsuspend is non-destructive).

### Moderator opens the unsuspend modal and confirms

1. The moderator clicks the "Unsuspend {username}" button (previously toggled by a prior suspension).
2. The same `toggleSuspendUserModal` flow runs with `modalContentSelector="#unsuspend-modal-content"`.
3. The moderator provides a reason and clicks `submit-user-unsuspend-btn`.
4. `suspendOrUnsuspendUser` is called with `btnAction="unsuspend"`, sending `user_status: "Good standing"` in the PATCH request.
5. On success, the trigger button is rewritten back to "Suspend {username}" with the `c-btn--destructive` class restored.

### Moderator attempts to submit without a reason

1. The moderator clicks the confirm button without filling in the reason textarea.
2. `checkReason` detects an empty value and sets the error paragraph's text to `"You must give a reason for this action."`.
3. No API request is made; the modal remains open for the moderator to correct the input.

## Failures / Exceptions

- If the PATCH request returns a response with `success: false`, a snackbar displays `"Error: something went wrong."` and the button state is not toggled.
- If the network request itself throws (e.g., connectivity failure), the caught error is formatted into a snackbar message as `"Error: {error}"` and no state update occurs.
