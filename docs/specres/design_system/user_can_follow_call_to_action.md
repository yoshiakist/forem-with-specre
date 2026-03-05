---
id: "01KJXZBTG4D34B5NGNH7T7AKA7"
name: "user_can_follow_call_to_action"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/javascript/crayons/CTAs/CTA.jsx`
- `app/javascript/crayons/CTAs/index.js`
- `app/javascript/crayons/CTAs/__tests__/CTA.test.jsx` (Test)

## Functional Overview

The `CTA` component renders a prominent call-to-action as an anchor element (`<a>`). It supports two visual variants — `default` and `branded` — and can optionally render an SVG icon to the left of the label text. CSS class names are composed dynamically based on the active variant, the presence of an icon alongside children, and any additional `className` provided by the caller. All extra HTML props are forwarded directly to the underlying anchor, allowing consumers to attach event handlers, `data-*` attributes, or ARIA attributes without modification to the component.

## Design Intent

The component is intentionally thin: it owns only the class-name composition and the icon slot, delegating navigation semantics entirely to the native `<a>` element. This keeps it accessible by default (no ARIA role overrides, no button-pretending-to-be-a-link) and makes it trivially testable with `axe`.

## Key Members

- `href: string` — destination URL; defaults to `'#'` when not supplied
- `variant: 'default' | 'branded'` — controls the visual style; `default` applies no variant modifier class
- `icon: elementType` — optional SVG source passed to the `<Icon>` sub-component; when present alongside `children`, the `c-cta--icon-left` class is added
- `className: string` — additional CSS classes merged into the root anchor element
- `children` — required label content rendered inside the anchor

## Scenarios

### User clicks the default CTA

1. The component renders an `<a>` element with the base class `c-cta` and no variant modifier.
2. No icon element is present in the DOM.
3. Clicking the link navigates the user to the URL specified by `href`.

### User clicks the branded CTA

1. The component receives `variant="branded"`.
2. The rendered `<a>` element carries both `c-cta` and `c-cta--branded` classes.
3. Clicking the link navigates the user to the URL specified by `href`.

### CTA renders with an icon alongside label text

1. The component receives an `icon` prop (an SVG element type) and non-empty `children`.
2. An `<Icon>` element is rendered to the left of the label, marked `aria-hidden="true"` and `focusable="false"` so it is invisible to assistive technology.
3. The root anchor gains the `c-cta--icon-left` class, positioning the icon correctly via CSS.

### CTA meets accessibility requirements

1. The component is rendered in any supported variant (default or branded) with visible label text.
2. An automated accessibility audit (`axe`) reports zero violations for both variants.
