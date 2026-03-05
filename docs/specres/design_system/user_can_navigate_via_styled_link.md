---
id: "01KJXZ9CSVRBRJJYMZHDJRHHFD"
name: "user_can_navigate_via_styled_link"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/javascript/crayons/Links/Link.jsx`
- `app/javascript/crayons/Links/index.js`
- `app/javascript/crayons/Links/__tests__/Link.test.jsx` (Test)

## Functional Overview

The `Link` component renders an HTML anchor element with a consistent set of design-system CSS classes, allowing users to navigate to a destination URL while benefiting from configurable visual variants. Callers may select a `branded` color variant, enable `block` display for full-width layout, apply `rounded` pill corners, and optionally prepend an SVG icon — either alongside text (`c-link--icon-left`) or as a standalone icon-only button (`c-link--icon-alone`). Additional class names and arbitrary HTML attributes are forwarded directly to the underlying `<a>` element, making the component both composable and accessible.

## Design Intent

The component centralises link styling so that all navigation elements in the application use the same CSS class tokens (`c-link`, `c-link--branded`, `c-link--block`, etc.) regardless of the call-site. Variant logic is kept in one place, preventing class-name drift across features. The icon is always marked `aria-hidden` and `focusable="false"` to ensure screen readers treat it as decorative, preserving the accessible name derived from the link text.

## Key Members

- `href: string` — destination URL; defaults to `#` when omitted
- `variant: 'default' | 'branded'` — controls colour treatment; `default` applies no variant modifier class
- `block: boolean` — adds `c-link--block` for full-width display
- `rounded: boolean` — adds `radius-full` for pill-shaped corners
- `icon: elementType` — SVG icon component; when provided without children the `c-link--icon-alone` class is applied; when provided with children `c-link--icon-left` is applied instead
- `className: string` — additional CSS classes merged into the class list

## Scenarios

### Rendering a default link

1. A caller renders `<Link href="/url">Label</Link>` with no additional props.
2. The component produces an `<a>` element with class `c-link` and the given `href`.
3. No variant, block, rounded, or icon modifier classes are added.

### Rendering a branded link

1. A caller renders `<Link variant="branded" href="/url">Label</Link>`.
2. The component adds the `c-link--branded` modifier class alongside `c-link`.
3. The anchor navigates to the given URL with the branded colour style applied.

### Rendering a block link

1. A caller renders `<Link block href="/url">Label</Link>`.
2. The component adds `c-link--block` to stretch the anchor to its container width.

### Rendering a link with an icon alongside text

1. A caller renders `<Link icon={SomeIcon} href="/url">Label</Link>`.
2. The component renders the icon as an `<Icon>` element marked `aria-hidden` before the text.
3. The `c-link--icon-left` modifier class is applied so spacing between icon and label is correct.

### Rendering a standalone icon-only link

1. A caller renders `<Link icon={SomeIcon} href="/url" />` with no children.
2. The component applies `c-link--icon-alone` instead of `c-link--icon-left`.
3. No text node is rendered; the icon constitutes the entire visual content of the anchor.
