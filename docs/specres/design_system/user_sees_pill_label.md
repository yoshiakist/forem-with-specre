---
id: "01KJXZM146W8F3KS8GR4RGT5B5"
name: "user_sees_pill_label"
status: "draft"
---

## Related Files

- `app/javascript/crayons/Pills/Pill.jsx`
- `app/javascript/crayons/Pills/index.js`

## Functional Overview

The `Pill` component renders a compact, button-based label element used throughout the design system to display a short text value. It optionally prefixes the label with a description icon, appends an action icon or a destructive-action icon (which always renders as an "X"), and can show a tooltip on hover. When `noAction` is set the button becomes visually inert (no click handler, `aria-disabled` attribute), and the cursor changes to `cursor-help` when a tooltip is also present. Keyboard users can dismiss the tooltip by pressing Escape, which suppresses the tooltip content via a CSS class toggle. The component's `children` prop carries the visible label text and is the only required prop.

## Design Intent

Rendering the pill as a `<button>` rather than a `<span>` or `<div>` gives interactive pills (remove tags, trigger actions) correct keyboard focus and native click semantics without extra ARIA role declarations. The `noAction` flag lets the same element be used in read-only contexts while sharing all visual styles, avoiding a separate display-only component. Tooltip suppression on Escape follows standard accessibility guidance for dismissible overlays (WCAG 2.1 SC 1.4.13).

## Key Members

- `children: string` (required) — the visible text label rendered inside the pill
- `descriptionIcon: elementType` — SVG component rendered before the label text at 18x18px
- `actionIcon: elementType` — SVG component rendered after the label text at 18x18px
- `destructiveActionIcon: bool` — when true, renders the built-in X icon as the action icon and applies the destructive modifier class
- `noAction: bool` — disables click handling and sets `aria-disabled`; changes cursor to `cursor-default` (or `cursor-help` when a tooltip is also provided)
- `tooltip: string | node` — content rendered in a hidden tooltip span; shown on hover/focus and suppressed via `crayons-tooltip__suppressed` when Escape is pressed
- `onKeyUp: function` — forwarded keyboard event handler, called before the internal Escape-suppression logic
- `onClick: function` — click handler, ignored when `noAction` is true

## Scenarios

### User views a plain label pill

1. A pill is rendered with only a `children` text prop (e.g., "JavaScript").
2. The component outputs a `<button>` element with class `c-pill` containing the text.
3. No icon or tooltip elements are present in the output.

### User views a pill with a description icon

1. A pill is rendered with `children` text and a `descriptionIcon` SVG component.
2. The `c-pill--description-icon` modifier class is applied to the button.
3. An `<Icon>` element appears before the label text, marked `aria-hidden` and non-focusable.

### User views a pill with an action icon

1. A pill is rendered with `children` text and an `actionIcon` SVG component.
2. The `c-pill--action-icon` modifier class is applied to the button.
3. An `<Icon>` element appears after the label text, marked `aria-hidden` and non-focusable.

### User views a destructive-action pill

1. A pill is rendered with `destructiveActionIcon` set to `true`.
2. Both `c-pill--action-icon` and `c-pill--action-icon--destructive` modifier classes are applied.
3. The built-in X (`XIcon`) SVG is rendered as the action icon instead of a custom one.

### User dismisses a tooltip by pressing Escape

1. A pill is rendered with a `tooltip` prop.
2. The button receives class `crayons-tooltip__activator` and a sibling `<span>` containing the tooltip text is rendered.
3. The user presses Escape while the pill has keyboard focus.
4. The tooltip span receives the `crayons-tooltip__suppressed` class, visually hiding it.
5. Pressing any other key or triggering a new interaction leaves the suppression state unchanged until Escape is pressed again.
