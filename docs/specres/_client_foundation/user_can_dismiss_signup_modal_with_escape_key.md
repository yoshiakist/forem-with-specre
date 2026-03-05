---
id: "01KJXY5CWN4BK1KR7CFWVB6542"
name: "user_can_dismiss_signup_modal_with_escape_key"
status: "draft"
---

## Related Files

- `app/javascript/packs/signupModalShortcuts.jsx`

## Functional Overview

When the global sign-up modal is present on the page, the application registers a keyboard shortcut so that pressing the Escape key hides the modal. A `KeyboardShortcuts` component is mounted into the modal's root element on `DOMContentLoaded`, and whenever the Escape key is pressed the modal element receives a `hidden` CSS class, causing it to disappear immediately without requiring a button click or pointer interaction.

## Design Intent

Rendering the `KeyboardShortcuts` component directly inside the `#global-signup-modal` container ties the keyboard listener's lifecycle to the modal's presence in the DOM. Using a CSS class (`hidden`) rather than removing the element from the DOM keeps the modal available for re-display if needed and avoids re-rendering costs. Delegating the shortcut wiring to the shared `KeyboardShortcuts` component enforces a consistent keyboard-shortcut pattern across the application.

## Key Members

- `global-signup-modal` — ID of the modal container element; used both as the React render root and as the target element to hide
- `KeyboardShortcuts` — shared Preact component that binds a map of key names to callback functions as keyboard event listeners
- `Escape` — the keyboard key whose press triggers modal dismissal
- `hidden` — CSS class added to the modal element to conceal it

## Scenarios

### User dismisses the modal with the Escape key

1. The page loads and the `#global-signup-modal` element is present in the DOM.
2. The `KeyboardShortcuts` component mounts inside the modal container, registering an `Escape` key handler.
3. While the modal is visible, the user presses the Escape key.
4. The handler locates the `#global-signup-modal` element and adds the `hidden` CSS class to it.
5. The modal is no longer visible to the user.

## Failures / Exceptions

- If `#global-signup-modal` is absent from the DOM when the script runs, the component is not mounted and no keyboard shortcut is registered.
- If `#global-signup-modal` cannot be found at the moment the Escape key is pressed (e.g., the element was removed after mount), the optional chaining (`?.`) prevents a runtime error and the operation is silently skipped.
