---
id: "01KJXZH48PEHNCY5DBFZRERMG4"
name: "user_can_wrap_input_with_form_field"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/javascript/crayons/formElements/FormField/FormField.jsx`
- `app/javascript/crayons/formElements/FormField/index.js`
- `app/javascript/crayons/formElements/FormField/__tests__/FormField.test.jsx` (Test)

## Functional Overview

`FormField` is a Preact wrapper component that renders a `div` with the `crayons-field` CSS class, providing a consistent labeled container for any form input. When a `variant` prop of `"radio"` or `"checkbox"` is supplied, the component appends the modifier class `crayons-field--radio` or `crayons-field--checkbox`, enabling the additional CSS layout rules required for those input types. All other form elements (text, select, textarea, etc.) omit the variant and receive only the base class.

## Design Intent

Only radio buttons and checkboxes require an extra modifier CSS class for correct visual layout — other form controls use the base `crayons-field` container without modification. By centralising this conditional class logic inside `FormField`, consuming components never need to construct the class string themselves, keeping the variant contract explicit and typed via PropTypes.

## Key Members

- `children` (required) — One or more child elements (typically a label and an input) to render inside the field container.
- `variant: 'radio' | 'checkbox' | undefined` — Optional modifier that appends `crayons-field--<variant>` to the container class. Defaults to `undefined` (no modifier).

## Scenarios

### Rendering a plain form field with no variant

1. A developer renders `<FormField>` wrapping any standard input (e.g., a text input and its label) without passing a `variant` prop.
2. The component renders a `div` with exactly the class `crayons-field`.
3. No modifier class is appended.

### Rendering a radio-button field

1. A developer renders `<FormField variant="radio">` wrapping a `RadioButton` element and its associated `<label>`.
2. The component renders a `div` with the classes `crayons-field crayons-field--radio`.
3. The CSS modifier enables the side-by-side layout expected for radio inputs.

### Rendering a checkbox field

1. A developer renders `<FormField variant="checkbox">` wrapping a checkbox input and its associated `<label>`.
2. The component renders a `div` with the classes `crayons-field crayons-field--checkbox`.
3. The CSS modifier enables the side-by-side layout expected for checkbox inputs.

### Maintaining accessibility when rendered with interactive content

1. A developer composes `<FormField>` with a focusable input and a programmatically associated `<label>` (via `htmlFor` / `id` pairing).
2. The rendered output has no accessibility violations as reported by automated axe analysis.
