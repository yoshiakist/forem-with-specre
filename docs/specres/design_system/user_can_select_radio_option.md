---
id: "01KJXZH4Z25EJA726891E3RW97"
name: "user_can_select_radio_option"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/javascript/crayons/formElements/RadioButton/RadioButton.jsx`
- `app/javascript/crayons/formElements/RadioButton/index.js`
- `app/javascript/crayons/formElements/RadioButton/__tests__/RadioButton.test.jsx` (Test)

## Functional Overview

The `RadioButton` component renders a styled HTML radio input element within the Crayons design system. It applies the `crayons-radio` CSS class by default, optionally appending any extra `className` provided by the caller. The component accepts a required `value` prop and an `onClick` handler, supports a controlled `checked` state, and forwards any additional props directly to the underlying `<input>` element. It is assumed to always be paired with an external `<label>` element for accessibility.

## Design Intent

The component is intentionally minimal — a thin wrapper around a native `<input type="radio">` — so that Crayons consumers get consistent styling without losing access to any native input attribute. Accessibility labelling responsibility is deliberately delegated to the parent, keeping this component single-purpose and composable.

## Key Members

- `value: string` (required) — the value submitted when this option is selected
- `onClick: function` (required) — callback invoked when the user clicks the radio button
- `checked: bool` — controls whether the input is in a selected state; defaults to `false`
- `id: string` — optional HTML id, used to associate with a `<label for="...">` in the parent
- `name: string` — optional radio group name that links mutually exclusive options
- `className: string` — optional extra CSS classes appended after `crayons-radio`

## Scenarios

### User sees an unchecked radio button by default

1. A parent component renders `<RadioButton value="opt" onClick={handler} />` without passing `checked`.
2. The component renders an `<input type="radio">` with `checked` set to `false`.
3. The input carries the CSS class `crayons-radio` with no additional classes.

### User sees a checked radio button when the checked prop is true

1. A parent component renders `<RadioButton value="opt" onClick={handler} checked />`.
2. The component renders an `<input type="radio">` with `checked` set to `true`.
3. The visual state reflects a selected option.

### User sees custom styling and identity props applied to the radio input

1. A parent renders `<RadioButton id="my-id" value="opt" name="my-group" className="extra-class" onClick={handler} />`.
2. The component forwards `id`, `value`, and `name` directly to the underlying input element.
3. The CSS class on the input is `crayons-radio extra-class` (base class followed by the extra class).

### User triggers the onClick handler by clicking the radio button

1. A parent renders a `RadioButton` with an `onClick` callback and a `data-testid` attribute.
2. The user clicks the rendered radio input.
3. The `onClick` callback is invoked at least once.
