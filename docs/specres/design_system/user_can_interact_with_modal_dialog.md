---
id: "01KJXZC4RF6CQF1P2CKHBY06GZ"
name: "user_can_interact_with_modal_dialog"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/javascript/crayons/Modal/Modal.jsx`
- `app/javascript/crayons/Modal/index.js`
- `app/javascript/crayons/Modal/__tests__/Modal.test.jsx` (Test)

## Functional Overview

The Modal component renders an accessible dialog overlay that traps keyboard focus within its boundaries until it is dismissed. It accepts a required title rendered in a header, an optional close button, configurable size variants (small, medium, large), an optional backdrop that can be made dismissible by clicking outside, a sheet mode for slide-in panel presentation with configurable alignment, and a prompt variant for confirmation dialogs. Focus is confined to the modal box by default, or to a caller-specified CSS selector, and is released when the modal closes. The component delegates focus trap lifecycle events to the `FocusTrap` shared component and calls the provided `onClose` callback when dismissed via the close button, the Escape key, or an outside click (if `backdropDismissible` is enabled).

## Design Intent

The component is built around ARIA best-practice: the inner box carries `role="dialog"` and `aria-modal="true"` so assistive technologies treat the overlay as a modal context. Focus trapping is delegated to a dedicated `FocusTrap` primitive rather than implemented inline, keeping the Modal responsible only for layout and configuration. Backdrop dismissal is opt-in (`backdropDismissible=false` by default) to prevent accidental data loss when a modal contains a form. The `focusTrapSelector` escape hatch lets callers restrict focus to a sub-region when the modal body contains intentionally unreachable controls outside the primary task area.

## Key Members

- `title: string` (required) — text displayed in the modal header and serves as the accessible label
- `onClose: func` — callback invoked whenever the modal is dismissed; defaults to a no-op
- `size: 'small' | 'medium' | 'large'` — controls the CSS width modifier; medium is the default and adds no extra class
- `backdropDismissible: bool` — when true, clicking outside the dialog box triggers `onClose`; defaults to false
- `noBackdrop: bool` — suppresses rendering of the `.crayons-modal__backdrop` overlay element
- `showHeader: bool` — controls visibility of the header bar (title + close button); defaults to true
- `sheet: bool` — activates sheet (slide-in panel) presentation mode
- `sheetAlign: 'center' | 'left' | 'right'` — controls sheet alignment; center is the default and adds no extra class
- `prompt: bool` — activates the prompt (confirmation dialog) size variant
- `centered: bool` — centers the prompt dialog vertically when combined with `prompt`
- `focusTrapSelector: string` — CSS selector for the focus trap boundary; defaults to `'.crayons-modal__box'`
- `allowOverflow: bool` — allows content to overflow the modal box (useful for dropdowns inside the modal)
- `className: string` — additional CSS class appended to the outermost container

## Scenarios

### User opens a modal and focus is trapped inside

1. A modal is rendered with at least one focusable element in its body.
2. Focus is automatically placed on the first focusable element within the modal (the close button by default).
3. Pressing Tab cycles focus only among focusable elements inside the modal box.
4. Elements outside the modal cannot receive focus while the modal is open.

### User dismisses the modal with the close button

1. The modal is rendered with an `onClose` callback and the default header visible.
2. The user clicks the close button (aria-label "Close") in the header.
3. The `onClose` callback is invoked exactly once.

### User dismisses the modal with the Escape key

1. The modal is rendered with an `onClose` callback.
2. The user presses the Escape key.
3. The `onClose` callback is invoked exactly once.

### User cannot dismiss by clicking outside when backdropDismissible is false (default)

1. The modal is rendered without the `backdropDismissible` prop (defaults to false).
2. The user clicks on content outside the modal dialog box.
3. The `onClose` callback is not called and the modal remains open.

### User dismisses the modal by clicking outside when backdropDismissible is enabled

1. The modal is rendered with `backdropDismissible` set to true.
2. The user clicks on content outside the modal dialog box.
3. The `onClose` callback is invoked exactly once.

### Modal renders with configurable size

1. The modal is rendered with a `size` prop set to `"large"`.
2. The outermost container element receives the CSS class `crayons-modal--large`.
3. A size of `"medium"` (the default) adds no size modifier class.

### Modal meets accessibility requirements

1. The modal is rendered with a title and body content.
2. The inner dialog element carries `role="dialog"` and `aria-modal="true"`.
3. An automated accessibility audit (axe) reports no violations.
