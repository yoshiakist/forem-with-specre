---
id: "01KJXZE8C35KFNQN3YR072APSX"
name: "user_can_pick_color_from_palette"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/javascript/crayons/formElements/ColorPicker/ColorPicker.jsx`
- `app/javascript/crayons/formElements/ColorPicker/index.js`
- `app/javascript/crayons/formElements/ColorPicker/__tests__/ColorPicker.test.jsx` (Test)

## Functional Overview

The `ColorPicker` component renders a hex color picker widget composed of three parts: a swatch button that toggles a dropdown palette, a hex text input prefixed with `#` for direct keyboard entry, and an optional clear button that appears whenever a color is selected. The color palette is powered by `react-colorful`'s `HexColorPicker` and is displayed in a dropdown popover managed by the shared `initializeDropdown` utility. The component maintains its selected color in local state initialized from an optional `defaultValue` prop. Any change — whether made through the palette or the text field — fires an `onChange` callback with the current hex string. A hidden `<input>` carries the form field value so the color can be submitted as part of an HTML form without the hex input field interfering with the `name` attribute.

## Design Intent

Three-character shorthand hex codes (e.g. `#0B6`) are valid CSS but can cause inconsistency downstream. On blur the component normalizes any three-character value to its six-character equivalent (e.g. `#00BB66`) so the rest of the application always receives a canonical, full-length hex string.

The swatch button's background color mirrors the current selection, giving the user an immediate live preview of the chosen color. When no color is selected the button renders with a dashed border to indicate an empty state rather than defaulting to black.

A hidden input is used for form submission to decouple the visible text field (which must not carry a `name` attribute that would submit duplicate values) from the actual form value.

## Key Members

- `id: string` — required; base identifier used to derive unique IDs for the trigger button (`color-popover-btn-{id}`) and the dropdown popover (`color-popover-{id}`)
- `buttonLabelText: string` — required; accessible label for the swatch toggle button
- `defaultValue: string` — optional hex color string used to pre-populate the picker on mount
- `inputProps: object` — optional additional props forwarded to `HexColorInput`; the `name` key is extracted and redirected to the hidden input
- `onChange: function` — optional callback invoked with the current hex string whenever the color changes
- `onBlur: function` — optional callback invoked when the hex text field loses focus

## Scenarios

### User opens the color palette and selects a color

1. The component renders with a swatch button and an empty hex text field.
2. User clicks the swatch button; the dropdown popover containing the `HexColorPicker` palette opens.
3. User drags the color picker handle to a desired hue/saturation/lightness position.
4. The swatch button background and the hex text field update in real time to reflect the chosen color.
5. The `onChange` callback is called with the six-character hex string on each change.

### User types a hex code directly into the text field

1. The component renders with the hex text field focused.
2. User types a valid six-character hex code (e.g. `#ababab`).
3. The swatch button background updates to match the typed color.
4. The `onChange` callback is called with the hex string on each keystroke.

### User enters a shorthand three-character hex code and leaves the field

1. User types a three-character hex code (e.g. `#0B6`) into the text field.
2. User moves focus away from the field (blur event fires).
3. The component expands the shorthand to its full six-character equivalent (`#00BB66`).
4. The hex text field, swatch, and hidden input are all updated to the canonical value.
5. The `onChange` callback is called with the expanded six-character hex string.

### Component renders with a pre-populated default value

1. A parent component passes `defaultValue="#ababab"` when mounting `ColorPicker`.
2. The component renders with the swatch showing the pre-set color and the hex field pre-filled.
3. The hidden input carries the default value so it is included in any immediate form submission.

### User clears the selected color

1. A color is currently selected; the clear button (`✕`) is visible next to the hex input.
2. User clicks the clear button.
3. The color state is reset to an empty string.
4. The swatch reverts to the empty-state style (dashed border, transparent background).
5. The hex text field is cleared and the hidden input value becomes empty.
6. The `onChange` callback is called with an empty string.
