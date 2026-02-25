---
id: "01KJ9GWWKF62PQBKP13K74MPN0"
name: "system_displays_admin_feedback_messages"
status: "draft"
---

## Related Files

- `app/javascript/admin/controllers/snackbar_controller.js`
- `app/javascript/admin/controllers/alert_controller.js`
- `app/javascript/admin/controllers/notice_controller.js`
- `app/javascript/admin/messageUtilities.js`
- `app/javascript/packs/admin/flashMessages.js`
- `app/views/layouts/admin.html.erb` (notification zones embedded here; primary coverage in admin_navigates_admin_panel)

## Functional Overview

The admin interface provides a three-layer feedback system for communicating operation outcomes to administrators. Server-rendered flash messages appear as dismissible notice banners at the top of the main content area and are handled by the NoticeController. Client-side operations surface feedback through two mechanisms: a transient snackbar toast (managed by SnackbarController) that auto-dismisses after 3 seconds and is well-suited for non-critical confirmations, and inline alert banners (managed by AlertController) that persist in an alert zone until dismissed and are used for error and success states requiring attention. Both client-side channels are driven by custom DOM events — `snackbar:add` and `error:generate` — so any part of the admin UI can trigger feedback without direct coupling to the controller. The `messageUtilities.js` module exports `displayErrorAlert()` and `displaySnackbar()` as thin helpers that dispatch these events. Accessibility is addressed by programmatically focusing the first flash dismiss button on page load so screen reader users are made aware of server-rendered messages without relying on `aria-live` regions.

## Design Intent

The three channels are intentionally decoupled through custom DOM events. Any Stimulus controller, Preact component, or vanilla script can dispatch `snackbar:add` or `error:generate` without importing or referencing the feedback controllers directly. This keeps feedback logic isolated in dedicated controllers and lets the rest of the admin codebase trigger notifications with a single helper call. The snackbar's 3-second lifespan is appropriate for transient confirmations (e.g., "saved"), while persistent alert banners are reserved for states where the admin may need to read, copy, or act on the message before it disappears. Server-rendered flash messages bypass JavaScript entirely and are therefore resilient to JS failures; the `flashMessages.js` pack adds only the accessibility focus behavior on top of them.

## Key Members

- `snackbar:add` — Custom DOM event dispatched on `document`; `detail.message` carries the text to display; `detail.addCloseButton` (optional boolean) adds a manual dismiss button to the toast
- `error:generate` — Custom DOM event dispatched on `document`; `detail.alertMsg` carries the HTML or text content to render in the alert zone
- `displaySnackbar(message)` — Helper in `messageUtilities.js` that dispatches `snackbar:add`
- `displayErrorAlert(alertMsg)` — Helper in `messageUtilities.js` that dispatches `error:generate`
- `snackZoneTarget` — DOM element managed by SnackbarController where the Preact Snackbar is mounted
- `alertZoneTarget` — DOM element managed by AlertController where inline alert banners are injected
- `js-flash-close-btn` — CSS class used to locate the first flash dismiss button for programmatic focus

## Scenarios

### Server-rendered flash message on page load

1. The server sets a flash notice or alert (e.g., after a redirect following a form submission).
2. The admin layout renders the flash message as a dismissible banner inside the notice zone on the next page load.
3. The `flashMessages.js` pack runs and focuses the first element with class `js-flash-close-btn`.
4. Screen reader users hear the dismiss button announced, making them aware of the message without relying on `aria-live`.
5. The admin clicks or activates the dismiss button; the notice container is removed from the DOM.

### Snackbar toast for a transient client-side confirmation

1. An admin action (e.g., saving a setting via an API call) completes successfully.
2. The handling code calls `displaySnackbar('Changes saved')`, which dispatches a `snackbar:add` custom event on `document` with the message in `event.detail`.
3. The SnackbarController on `<body>` receives the event via `data-action="snackbar:add@document->snackbar#addItem"` and calls `addSnackbarItem` on the mounted Preact Snackbar component.
4. The snackbar toast appears in the snack zone with the message text.
5. After 3 seconds the toast automatically disappears without any admin interaction.

### Inline error alert for a failed client-side operation

1. An admin action fails (e.g., an API request returns an error).
2. The handling code calls `displayErrorAlert('Something went wrong')`, which dispatches an `error:generate` custom event on `document`.
3. The AlertController receives the event and injects a styled danger banner (using the `crayons-notice--danger` class) containing the message and a close icon into the `alertZoneTarget` element.
4. The banner persists in the alert zone, visible to the admin until they dismiss it.
5. The admin clicks the close icon; the `closeAlert` action fires and clears the `alertZoneTarget` innerHTML.

### Inline success alert for a client-side operation

1. A client-side operation completes and the code needs to display a persistent success confirmation.
2. A `success:generate` event (or direct controller call invoking `generateSuccessAlert`) is dispatched with an `alertMsg` in `event.detail`.
3. The AlertController injects a styled success banner (using the `crayons-notice--success` class) into the `alertZoneTarget`.
4. The banner persists until the admin dismisses it via the close icon.

## Failures / Exceptions

- If the Preact Snackbar module fails to load asynchronously, `addItem` will throw and no toast will appear; there is no fallback rendering.
- If the `alertZoneTarget` element is absent from the DOM (e.g., the controller is not connected), `generateErrorAlert` will throw a missing target error.
- Server-rendered flash messages are unaffected by JavaScript failures; only the programmatic focus behavior in `flashMessages.js` is lost if the script does not run.
- If `js-flash-close-btn` is not present in the DOM (no flash message), `firstFlashDismissBtn?.focus()` is a no-op due to optional chaining.
