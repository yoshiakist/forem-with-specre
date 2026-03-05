---
id: "01KJXXT4W5WS018D6C53D3JFD6"
name: "admin_customizes_branding_colors_with_picker"
status: "draft"
---

## Related Files

- `app/javascript/packs/enhanceColorPickers.jsx`
- `app/javascript/colorPickers/replaceTextInputWithColorPicker.jsx`

## Functional Overview

When an admin visits a branding configuration page, any plain text inputs marked with the `data-color-picker` attribute are automatically upgraded to interactive color picker components. The pack entry point queries the DOM for all such inputs and invokes a utility function for each one. That utility reads the input's existing attributes and current value, renders a Preact-based `ColorPicker` component in place of the original input using a root fragment to preserve DOM position, and then removes the original input element. The result is a richer color selection experience while retaining full form compatibility through the copied input attributes.

## Design Intent

The enhancement is applied progressively at page load so that the server-rendered form remains functional even if JavaScript fails to execute. Using a data attribute (`data-color-picker`) as the selector keeps the JavaScript decoupled from CSS class names or specific page structure. The `createRootFragment` helper is required because Preact cannot perform a virtual DOM diff that swaps one input for another, so the original input is removed manually after rendering.

## Key Members

- `data-color-picker` — data attribute that identifies text inputs to be upgraded to color pickers
- `labelText` — value read from `input.dataset.labelText`; forwarded to the `ColorPicker` component as `buttonLabelText`
- `inputProps` — a plain object populated by copying all DOM attributes from the original input; passed as `inputProps` to `ColorPicker` to preserve `name`, `id`, `value`, and any other attributes needed for form submission
- `ColorPicker` — Preact component from `@crayons` that renders the visual color picker UI
- `createRootFragment` — helper that anchors the Preact render root to the original input's position within its parent

## Scenarios

### Admin opens the branding color settings page

1. The browser loads the branding settings page, which contains one or more text inputs decorated with `data-color-picker`.
2. The `enhanceColorPickers` pack script runs after the DOM is ready.
3. The script queries for all `[data-color-picker]` elements and iterates over them.
4. For each input, `replaceTextInputWithColorPicker` is called with the input element and its `labelText` dataset value.
5. Each plain text input is replaced by a fully interactive `ColorPicker` component showing the previously saved color value.

### Color picker renders with the correct initial value

1. An existing branding color (e.g., `#FF6600`) is stored as the `value` attribute of a `[data-color-picker]` input when the page is rendered server-side.
2. The utility reads `input.value` and passes it to `ColorPicker` as `defaultValue`.
3. The color picker renders pre-filled with `#FF6600`, showing the saved color to the admin.

### All input attributes are preserved after enhancement

1. The original text input carries attributes such as `id`, `name`, and any `data-*` values required for form behavior.
2. The utility iterates `input.attributes` and copies every attribute into `inputProps`.
3. The `ColorPicker` component receives `inputProps`, ensuring the underlying hidden input retains the same `name` and `id` so the form submits correctly.

### Page contains no color picker inputs

1. The admin visits a settings page that has no elements with the `data-color-picker` attribute.
2. `document.querySelectorAll('[data-color-picker]')` returns an empty list.
3. The loop body never executes, and no errors are raised.

### Admin changes a color using the picker

1. The `ColorPicker` component is rendered and the admin interacts with it to select a new color.
2. The component updates its internal value and reflects the new color in the UI.
3. When the admin submits the branding form, the selected color value is included in the form payload under the original input's `name` attribute.
