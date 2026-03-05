---
id: "01KJXZBZ7SD70HBFWCDJ1GCTZB"
name: "user_can_open_dropdown_menu"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/javascript/crayons/Dropdown/Dropdown.jsx`
- `app/javascript/crayons/Dropdown/index.js`
- `app/javascript/crayons/Dropdown/__tests__/Dropdown.test.jsx` (Test)

## Functional Overview

The `Dropdown` component renders a toggleable container (`crayons-dropdown`) that wraps arbitrary children passed via composition. On first mount, the component calls `initializeDropdown` (from `@utilities/dropdownUtils`) to attach open/close click event listeners to a designated trigger button and, optionally, a close button placed inside the dropdown content. Optional `onOpen` and `onClose` callbacks allow callers to react to visibility changes. An optional `className` prop appends additional CSS classes to the container for positioning purposes.

## Design Intent

Separating event-listener setup from rendering lets any existing button in the DOM act as the trigger without coupling the trigger element to the dropdown's component tree. The one-time initialization guard (`isInitialized` state flag) prevents duplicate listener registration across re-renders while keeping the component stateless with respect to open/close state — that state is owned by the utility layer (`initializeDropdown`).

## Key Members

- `triggerButtonId: string` — DOM ID of the button that opens and closes the dropdown
- `dropdownContentId: string` — DOM ID applied to the rendered container element; used by `initializeDropdown` to locate the content node
- `dropdownContentCloseButtonId: string` (optional) — DOM ID of a button inside the dropdown that, when clicked, closes it
- `onOpen: () => void` (optional) — callback invoked when the dropdown opens
- `onClose: () => void` (optional) — callback invoked when the dropdown closes
- `className: string` (optional) — additional CSS classes appended to the `crayons-dropdown` root element
- `isInitialized: boolean` — internal state flag that ensures `initializeDropdown` is called exactly once per component instance

## Scenarios

### Dropdown renders its children inside the container

1. A parent renders `<Dropdown triggerButtonId="..." dropdownContentId="...">` with child content
2. The component outputs a `<div>` with the class `crayons-dropdown` containing the provided children
3. The rendered HTML is stable and matches the expected snapshot

### Dropdown renders with additional CSS classes

1. A parent passes a non-empty `className` prop (e.g., `"right-4 left-4"`)
2. The component appends the value to the root class attribute, producing `"crayons-dropdown right-4 left-4"`
3. Positioning or other custom styles take effect without affecting the base `crayons-dropdown` class

### Dropdown initializes open/close event listeners on first render

1. The component mounts with `triggerButtonId`, `dropdownContentId`, and optional `dropdownContentCloseButtonId`
2. On the first layout effect, `initializeDropdown` is called with those IDs along with the `onOpen` and `onClose` callbacks
3. The trigger button click toggles the dropdown's visibility and fires the appropriate callback
4. Subsequent re-renders do not re-register listeners because `isInitialized` is already `true`

### Dropdown invokes onOpen and onClose callbacks on visibility change

1. The dropdown is initialized and the trigger button is clicked
2. When the dropdown transitions to visible, the `onOpen` callback is invoked
3. When the dropdown transitions to hidden (via trigger button or close button), the `onClose` callback is invoked

### Dropdown meets accessibility requirements

1. The component is rendered with valid children
2. An automated accessibility audit (axe) is run against the rendered output
3. No accessibility violations are detected
