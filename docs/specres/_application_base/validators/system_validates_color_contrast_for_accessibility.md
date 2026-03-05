---
id: "01KJXNBDC10EP7TQ8TQ9Q9F4SX"
name: "system_validates_color_contrast_for_accessibility"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/validators/color_contrast_validator.rb`
- `app/services/color/accessibility.rb`
- `app/javascript/utilities/color/contrastValidator.js`
- `app/javascript/utilities/color/WCAGColorContrast.js`
- `app/javascript/utilities/__tests__/color/WCAGColorContrast.test.js` (Test)

## Functional Overview

The system enforces WCAG 2.0 color contrast accessibility requirements at both the server and client layers. On the server side, `ColorContrastValidator` is an ActiveModel validator that rejects attribute values whose contrast ratio against white falls below 4.5:1 (the WCAG AA threshold). It delegates the contrast calculation to `Color::Accessibility`, which uses the `WCAGColorContrast` Ruby gem. On the client side, the `WCAGColorContrast` JavaScript object implements the same WCAG 2.0 luminance formula directly, and `isLowContrast` wraps it with the same default threshold, enabling real-time contrast checks in the browser without a round-trip to the server.

## Design Intent

The 4.5:1 minimum contrast ratio and comparison against white (#ffffff) follow the WCAG 2.0 Level AA success criterion 1.4.3. Both layers share the same threshold and default compared color so that client-side feedback and server-side validation are consistent. Invalid hex strings (e.g. malformed colors) are silently ignored by the Rails validator because they are expected to be caught by an earlier format validator in the same model.

## Key Members

- `min_contrast` — the minimum acceptable contrast ratio; defaults to `4.5` (WCAG AA threshold)
- `compared_color` — the background color to compare against; defaults to `ffffff` (white)

## Scenarios

### Server rejects a hex color with insufficient contrast

1. A model attribute is declared with `ColorContrastValidator`.
2. The model is saved or validated with a hex color value.
3. The system strips the leading `#` and computes the WCAG 2.0 contrast ratio of the value against white.
4. If the ratio is below 4.5, the system adds a validation error to the attribute with the message from `validators.color_contrast_validator.must_be_darker`.
5. The record is not saved.

### Server accepts a hex color with sufficient contrast

1. A model attribute is declared with `ColorContrastValidator`.
2. The model is validated with a hex color that has a contrast ratio of 4.5 or higher against white.
3. No error is added to the attribute, and the record passes validation.

### Client determines whether a color has low contrast

1. JavaScript calls `isLowContrast(color)` with an optional `comparedColor` and `minContrast` (defaulting to `ffffff` and `4.5`).
2. The function strips any `#` prefix from both colors and calls `WCAGColorContrast.ratio`.
3. If the ratio is below `minContrast`, the function returns `true`; otherwise `false`.

### WCAG contrast ratio calculation

1. The system receives two hex color strings (3- or 6-character, without `#`).
2. Each hex value is converted to relative luminance using the WCAG 2.0 formula (sRGB linearization and weighted sum).
3. The contrast ratio is returned as `(lighter + 0.05) / (darker + 0.05)`, which equals 21 for black-on-white and 1 for identical colors.

### Invalid color input is rejected by the JavaScript layer

1. `WCAGColorContrast.ratio` is called with a hex string that does not match the 3- or 6-character hexadecimal pattern.
2. The function throws an exception identifying the invalid color value.

## Failures / Exceptions

- If the hex value passed to `ColorContrastValidator` is malformed, `WCAGColorContrast::InvalidColorError` is raised and silently rescued; no contrast error is added, allowing the format validator to handle it instead.
- If `WCAGColorContrast.ratio` in JavaScript receives an invalid hex string, it throws a string error (`"Invalid color <value>"`); callers are responsible for handling this exception.
