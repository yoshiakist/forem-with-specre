---
id: "01KHYB2J6VNGEBTQT0WTWQKDSW"
name: "organization_picker_renders_select_dropdown"
status: "draft"
last_verified: "2026-02-21"
---

## Related Files

- app/javascript/organization/OrganizationPicker.jsx

## Functional Overview

The OrganizationPicker is a Preact component that renders an HTML select dropdown for choosing an organization. It accepts a list of organizations, a currently selected organization ID, and a callback, and renders option elements with a leading empty/"None" option for deselection.

## Scenarios

### Picker renders organization options with selection state

1. The component renders a `<select>` element with an accessible "Select an organization" aria-label.
2. The first option is an empty-value option displaying the `emptyLabel` prop (defaults to "None").
3. Each organization in the `organizations` array is rendered as an `<option>` with its ID as the value and name as the display text.
4. The option matching the current `organizationId` is marked as selected.
5. If `organizationId` is null, the empty/none option is marked as selected.
6. The `onToggle` callback is invoked on the select element's blur event.
