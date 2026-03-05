---
id: "01KJXZE70RB82FADAFM5ZSKYH1"
name: "user_can_interact_with_mobile_drawer"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/javascript/crayons/MobileDrawer/MobileDrawer.jsx`
- `app/javascript/crayons/MobileDrawer/index.js`
- `app/javascript/crayons/MobileDrawer/__tests__/MobileDrawer.test.jsx` (Test)

## Functional Overview

The `MobileDrawer` component renders a full-width modal panel that slides in from the bottom of the viewport. When open, it displays a semi-transparent overlay behind the content panel, traps keyboard focus within the panel so that Tab cycles only through elements inside the drawer, and announces itself to screen readers via `role="dialog"` and `aria-label` set to the required `title` prop. Clicking outside the drawer content area or pressing Escape triggers the `onClose` callback, allowing the parent to unmount the drawer and restore normal interaction.

## Design Intent

The drawer is designed for mobile contexts where a bottom sheet pattern is more thumb-friendly than a centered modal. Focus trapping is handled by a shared `FocusTrap` component with `clickOutsideDeactivates` enabled, keeping the MobileDrawer implementation thin and delegating accessibility concerns to a reusable primitive. The `title` prop is surfaced only to assistive technology (via `aria-label`), not rendered visually, giving consumers full control over the drawer's visible heading markup through `children`.

## Key Members

- `title: string` (required) — Accessible label applied to the dialog element via `aria-label`; announced by screen readers when the drawer opens.
- `onClose: Function` (optional, defaults to no-op) — Called when the user dismisses the drawer by pressing Escape or clicking outside the content panel.
- `children: node` (required) — Arbitrary content rendered inside the drawer panel.
- `FocusTrap` — Shared component that manages focus containment; configured with `clickOutsideDeactivates` and `selector=".crayons-mobile-drawer__content"`.

## Scenarios

### Drawer renders with accessible markup

1. A parent component conditionally mounts `MobileDrawer`, passing a `title` string and child elements.
2. The drawer renders an overlay div and a content panel with `role="dialog"`, `aria-modal="true"`, and `aria-label` equal to the `title` prop.
3. Screen readers announce the dialog and its label immediately upon mount.

### Focus is trapped inside the drawer

1. The drawer mounts with multiple focusable elements inside and at least one focusable element outside.
2. Focus moves automatically to the first focusable element inside the drawer.
3. Pressing Tab cycles forward through focusable elements within the drawer, wrapping back to the first element after the last.
4. Focus never leaves the drawer content panel while it is open.

### Drawer closes when Escape is pressed

1. The drawer is open and focus is inside the content panel.
2. The user presses the Escape key.
3. The `onClose` callback is invoked, allowing the parent to unmount the drawer.

### Drawer closes when user clicks outside the content panel

1. The drawer is open and the user clicks on an element outside the `.crayons-mobile-drawer__content` panel (e.g., the overlay or surrounding page content).
2. The `FocusTrap` deactivates due to `clickOutsideDeactivates`.
3. The `onClose` callback is invoked, allowing the parent to unmount the drawer.

### Drawer has no accessibility violations

1. The drawer is rendered with a valid `title` and at least one focusable child element.
2. An automated accessibility audit (axe) finds no violations in the rendered output.
