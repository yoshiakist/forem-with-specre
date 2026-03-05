---
id: "01KJXZ9DWA0B3KQM84ZW3D4BBC"
name: "user_can_group_related_buttons"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/javascript/crayons/ButtonGroup/ButtonGroup.jsx`
- `app/javascript/crayons/ButtonGroup/index.js`
- `app/javascript/crayons/ButtonGroup/__tests__/ButtonGroup.test.jsx` (Test)

## Functional Overview

The `ButtonGroup` component renders a container that groups related buttons together as a single accessible unit. It wraps its children in a `<div>` with `role="group"` and an `aria-label` derived from the required `labelText` prop, ensuring assistive technologies can identify and describe the group to users. The component applies the `crayons-btn-group` CSS class for consistent design-system styling and re-exports its interface through the barrel `index.js` for convenient imports across the application.

## Design Intent

Using `role="group"` with an explicit `aria-label` follows ARIA best practices for grouping interactive controls. This allows screen readers to announce the group's purpose before enumerating individual buttons, which improves navigation for keyboard and assistive-technology users. Requiring `labelText` as a mandatory prop enforces accessible labeling at the component API level rather than relying on consumers to remember it.

## Key Members

- `labelText: string` (required) — Human-readable label passed to `aria-label`; describes the purpose of the button group to assistive technologies.
- `children: node` — One or more button elements rendered inside the group container.

## Scenarios

### Rendering a group of related buttons

1. A consumer renders `ButtonGroup` with a descriptive `labelText` and two or more `Button` children.
2. The component outputs a `<div>` container with `role="group"` and `aria-label` set to the provided `labelText`.
3. The `crayons-btn-group` CSS class is applied to the container for design-system styling.
4. All child buttons appear inside the container and retain their individual behavior.

### Providing accessible labeling to assistive technologies

1. A screen reader or accessibility tool encounters the button group in the DOM.
2. The tool reads `role="group"` and announces the group using the value of `aria-label`.
3. Users navigating with assistive technology understand the collective purpose of the buttons before interacting with any individual button.

### Passing an accessibility audit

1. A component is rendered with `ButtonGroup` wrapping one or more buttons, with a valid `labelText` provided.
2. An automated accessibility checker (such as `axe`) inspects the rendered output.
3. No accessibility violations are reported, confirming that the grouping and labeling structure meets WCAG requirements.
