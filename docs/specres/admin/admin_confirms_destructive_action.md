---
id: "01KJ9H04NFNKVCEGFVZ2SRPXF0"
name: "admin_confirms_destructive_action"
status: "draft"
---

## Related Files

- `app/javascript/admin/adminModal.js`
- `app/javascript/admin/controllers/modal_controller.js`
- `app/javascript/admin/controllers/confirmation_modal_controller.js`
- `app/views/admin/shared/_destroy_confirmation_modal.html.erb`

## Functional Overview

The admin interface provides a two-tier modal system for destructive operations. The generic `adminModal` utility renders a Crayons modal with a configurable title, body, and two action buttons, each wired to caller-supplied click handlers. For operations that are irreversible (deletes), the `ConfirmationModalController` (a Stimulus controller extending the base `ModalController`) requires the admin to type a specific sentence — "My username is @{username} and this action is 100% safe and appropriate." — before the DELETE request is dispatched. When the typed text matches exactly, the controller sends a DELETE fetch request to the target endpoint. Depending on the endpoint, it either removes the affected row from the DOM in place or stores an outcome message in `localStorage` and redirects the page. If the text does not match, a mismatch warning is revealed without closing the modal.

## Design Intent

Requiring the admin to type a full, personalized sentence (rather than clicking a simple "Are you sure?" button) makes it nearly impossible to trigger a destructive action by accident or by a misclick. The sentence includes the admin's own username, which further reduces the risk of a shared session being misused. This pattern is well-established in developer tooling (e.g., GitHub repository deletion) and directly reflects the principle that the cost of an extra confirmation step is far smaller than the cost of irreversible data loss.

## Key Members

- `confirmationText(username)` — Returns the exact sentence the admin must type: `"My username is @{username} and this action is 100% safe and appropriate."`
- `nonRedirectEndpoints` — List of endpoints where deletion is handled asynchronously by removing the DOM row without a full page reload.
- `redirectEndpoints` — List of endpoints where deletion triggers a page redirect after storing the outcome message in `localStorage`.
- `ConfirmationModalController.itemIdValue` — The ID of the record to be deleted, set from the triggering element's `data-item-id` attribute.
- `ConfirmationModalController.usernameValue` — The current admin's username, used to build the required confirmation sentence.
- `ConfirmationModalController.endpointValue` — The API endpoint path for the DELETE request.

## Scenarios

### Admin opens the confirmation modal

1. The admin clicks a delete button that has `data-action="confirmation-modal#openModal"` along with `data-item-id`, `data-endpoint`, and `data-username` attributes.
2. `ConfirmationModalController.openModal` reads these attributes and stores them as controller values.
3. The controller calls `toggleModal()`, which renders the `ModalController` Preact modal, injecting the server-rendered content from `_destroy_confirmation_modal.html.erb` into the modal body.
4. The modal displays the required confirmation sentence (personalized with the admin's username), an empty text input, a "Confirm changes" button, and a "Discard changes" button.

### Admin types the correct sentence and confirms

1. The admin types the full sentence exactly as shown: "My username is @{username} and this action is 100% safe and appropriate."
2. The admin clicks "Confirm changes", triggering `checkConfirmationText`.
3. The typed text matches the expected sentence, so the modal is closed and `sendToEndpoint` is called with the stored item ID and endpoint.
4. A DELETE request is sent to `{endpoint}/{itemId}` with CSRF token and JSON headers.
5. On a successful response, `handleRecord` determines whether to remove the row from the DOM (for `nonRedirectEndpoints`) or redirect the page after storing the outcome in `localStorage` (for `redirectEndpoints`).

### Admin types an incorrect sentence

1. The admin types text that does not exactly match the required confirmation sentence.
2. The admin clicks "Confirm changes", triggering `checkConfirmationText`.
3. The typed text does not match; the mismatch warning (`#mismatch-warning`) is unhidden via removal of the `hidden` class.
4. The modal remains open, the DELETE request is not sent, and the admin can correct their input or cancel.

### Admin cancels without confirming

1. The admin clicks "Discard changes" (or the modal dismiss button) without typing the confirmation sentence.
2. `closeModal` is called, which unmounts the Preact modal component by rendering `null` into the modal root.
3. No DELETE request is issued, and the resource remains unchanged.

## Failures / Exceptions

- If the DELETE request returns a non-OK HTTP response, the response JSON's `error` field is displayed via `displayErrorAlert` and the modal is closed.
- If the fetch itself throws a network error, the error message is displayed via `displayErrorAlert`.
- If the endpoint is not listed in either `nonRedirectEndpoints` or `redirectEndpoints`, `handleRecord` falls through and displays a generic "Something went wrong." error alert.
- On page load, if the URL contains the `redirected` query parameter and `localStorage` holds an `outcome` value, the stored message is displayed as a snackbar and then removed from storage.
