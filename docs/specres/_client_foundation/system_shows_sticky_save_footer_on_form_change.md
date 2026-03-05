---
id: "01KJXY820ZJX31KDY0WV8424R4"
name: "system_shows_sticky_save_footer_on_form_change"
status: "draft"
---

## Related Files

- `app/javascript/packs/stickySaveFooter.js`

## Functional Overview

When any input within a form marked with the class `sticky-footer-form` changes, the system makes the page's save footer element visible and sticky. This is achieved by appending CSS utility classes (`sticky`, `z-sticky`, `bottom-0`) to the element bearing the class `save-footer`, which causes it to affix to the bottom of the viewport so the user can save their changes without scrolling.

## Design Intent

The save footer is hidden or non-sticky by default to avoid cluttering the UI until the user actually modifies something. Responding to the form's `change` event (which bubbles up from any child input) keeps the logic minimal and does not require tracking individual fields. Applying classes rather than inline styles keeps the presentation layer consistent with the application's utility-class CSS system.

## Key Members

- `sticky-footer-form` — CSS class that designates the form whose changes are monitored
- `save-footer` — CSS class that identifies the footer element to be made sticky
- `sticky`, `z-sticky`, `bottom-0` — utility CSS classes added to pin the footer to the bottom of the viewport

## Scenarios

### User edits a field inside the tracked form

1. The page loads with a form element carrying the class `sticky-footer-form` and a footer element carrying the class `save-footer`.
2. The user interacts with any input inside the form, triggering a `change` event.
3. The system detects the event and locates the `save-footer` element.
4. The system adds the `sticky`, `z-sticky`, and `bottom-0` classes to the footer element.
5. The footer becomes fixed to the bottom of the viewport, remaining visible as the user scrolls.

## Failures / Exceptions

- If no element with the class `save-footer` exists in the DOM at the time of the `change` event, the footer is silently not modified (the `if (saveFooter)` guard prevents a null-reference error).
- If no element with the class `sticky-footer-form` is present on the page when the script executes, accessing index `[0]` returns `undefined` and calling `addEventListener` on it will throw a runtime error. The script assumes such a form is always present when this pack is loaded.
