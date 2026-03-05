---
id: "01KJXZKK9VT55P2Y3HEE9044KS"
name: "user_sees_icon_in_interface"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/javascript/crayons/Icons/Icon.jsx` (Frontend component)
- `app/javascript/crayons/Icons/index.js` (Frontend export)
- `app/helpers/crayons_helper.rb` (Backend helper)
- `spec/helpers/crayons_helper_spec.rb` (Test)

## Functional Overview

The Crayons design system provides a unified icon rendering primitive used across both the frontend and backend. On the frontend, the `Icon` Preact component accepts an SVG source component and renders it with the `crayons-icon` CSS class, optionally adding `crayons-icon--default` when native (non-inherited) color is desired. On the backend, the `crayons_icon_tag` Ruby helper wraps `inline_svg_tag` to produce an accessible inline SVG element with the same CSS class contract, defaulting to 24×24 pixels and enabling ARIA attributes automatically. Both surfaces use the same class names so icons look and behave consistently regardless of how they are rendered.

## Design Intent

A single `crayons-icon` CSS class is the contract between the specification and the stylesheet. By converging on this class name in both the Preact component and the Rails helper, the design system enforces visual consistency without duplicating styling logic. The `crayons-icon--default` modifier intentionally opts the icon out of CSS `currentColor` inheritance so that icons with their own embedded colors (such as emoji or brand assets) are rendered faithfully rather than tinted by surrounding text.

## Key Members

- `src: elementType` — Required. The SVG component to render (frontend only).
- `native: Boolean` — Optional (default `false`). When `true`, adds `crayons-icon--default` to prevent color inheritance from the parent element.
- `className: String` — Optional. Additional CSS classes to append (frontend).
- `class: String` — Optional. Additional CSS classes to append (backend).
- `name: String | Symbol` — The icon file name; `.svg` extension is appended automatically if absent (backend only).
- Default dimensions `width: 24, height: 24` are applied by the backend helper unless overridden.

## Scenarios

### Frontend renders an icon with base class

1. A page or component imports `Icon` from the Crayons Icons package and provides an SVG source component via the `src` prop.
2. The `Icon` component renders the SVG with the `crayons-icon` CSS class applied.
3. The icon inherits its color from the surrounding text via CSS `currentColor`.

### Frontend renders an icon in native color mode

1. A component renders `Icon` with `native={true}` and an SVG source that contains its own embedded colors.
2. The `Icon` component adds both `crayons-icon` and `crayons-icon--default` CSS classes.
3. The icon displays its own colors rather than inheriting from the parent element.

### Frontend renders an icon with additional CSS classes

1. A component renders `Icon` passing a custom `className` alongside the required `src` prop.
2. The `Icon` component merges `crayons-icon` and the custom class together using `classNames`.
3. The rendered SVG carries all specified classes.

### Backend renders an accessible inline SVG icon

1. A Rails view calls `crayons_icon_tag` with an icon name (string or symbol, with or without `.svg` suffix).
2. The helper normalises the name to include `.svg`, assembles a class string starting with `crayons-icon`, and delegates to `inline_svg_tag` with ARIA enabled and default 24×24 dimensions.
3. The resulting HTML is a self-contained `<svg>` element with `role="img"` and the `crayons-icon` class.

### Backend renders an icon with native color and extra classes

1. A Rails view calls `crayons_icon_tag` with `native: true` and an additional `:class` option.
2. The helper builds the class string as `"crayons-icon crayons-icon--default <extra_class>"`.
3. The rendered SVG carries all three classes in that order.
