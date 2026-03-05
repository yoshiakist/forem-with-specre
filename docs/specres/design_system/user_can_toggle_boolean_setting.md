---
id: "01KJXZHA0MNZG1M31EXQKE9VX8"
name: "user_can_toggle_boolean_setting"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/javascript/crayons/formElements/Toggles/Toggle.jsx`
- `app/javascript/crayons/formElements/Toggles/index.js`
- `app/javascript/crayons/formElements/Toggles/__tests__/Toggle.test.jsx` (Test)

## Functional Overview

The `Toggle` component renders a styled checkbox input (`<input type="checkbox" className="c-toggle">`) that visually presents a boolean on/off switch to the user. It forwards all provided props directly to the underlying input element, allowing consumers to control checked state, disabled state, event handlers, and any other standard HTML input attributes. The component is exported from the Toggles module and available throughout the Crayons design system.

## Design Intent

The Toggle is implemented as a thin wrapper around a native HTML checkbox input rather than a custom interactive widget. This approach preserves native browser accessibility semantics (keyboard navigation, screen-reader announcements, form participation) without requiring additional ARIA attributes. By spreading all props onto the underlying input, the component remains composable and avoids encoding assumptions about usage context.

## Key Members

- `className: "c-toggle"` — CSS class applied to the input, which drives the visual toggle appearance via stylesheet rules
- `...otherProps` — all additional props (e.g., `checked`, `disabled`, `onChange`, `id`, `name`) are forwarded directly to the `<input>` element

## Scenarios

### Default render

1. A consumer renders `<Toggle />` with no props.
2. The component outputs a single `<input type="checkbox">` element with the `c-toggle` class and no other attributes.

### Toggle rendered inside an associated label

1. A consumer wraps `<Toggle />` inside a `<label>` element that provides visible text.
2. The rendered markup contains no accessibility violations: the checkbox is programmatically associated with its label and is reachable by assistive technologies.

### Toggle rendered with additional HTML input props

1. A consumer renders `<Toggle disabled={true} className="example-class" />`.
2. The component forwards both the `disabled` attribute and the extra `className` to the underlying `<input>` element, merging them with the default `c-toggle` class as provided by the consumer.

### Toggle used as a controlled input

1. A consumer renders `<Toggle checked={true} onChange={handler} />`.
2. The component passes `checked` and `onChange` through to the native input, making it a controlled checkbox that reflects the consumer's state.

## Failures / Exceptions

- Rendering `<Toggle />` without an associated label or `aria-label` attribute produces an accessible-but-unlabelled control; accessibility audit tools will flag this as a violation when the toggle is not wrapped in a label.
