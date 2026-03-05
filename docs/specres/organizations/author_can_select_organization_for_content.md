---
id: "01KJ02KZ1T0N31A9EEK1JXA2YS"
name: "author_can_select_organization_for_content"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/javascript/organization/OrganizationPicker.jsx`
- `app/javascript/organization/__tests__/OrganizationPicker.test.jsx` (Test)

## Functional Overview

When an author creates or edits content, they can associate that content with one of their organizations by choosing from a dropdown list of the organizations they belong to. The `OrganizationPicker` component renders a `<select>` element populated with all available organizations plus a configurable empty option (defaulting to "None"). Whichever organization matches the current `organizationId` prop is pre-selected; when no organization ID is provided the empty option is selected instead. Whenever the author leaves the picker, a callback is invoked so the parent form can respond to the change.

## Key Members

- `organizations` — array of organization objects (each with `id` and `name`) available for selection
- `organizationId` — the ID of the currently selected organization, or `null`/`undefined` for no selection
- `emptyLabel` — label text for the "no organization" option; defaults to `"None"`
- `onToggle` — callback fired on `blur` when the author moves focus away from the picker

## Scenarios

### Author selects an organization from the list

1. The author opens a content creation or editing form that includes an `OrganizationPicker`.
2. The picker renders a dropdown listing all organizations the author belongs to, plus a "None" option at the top.
3. The organization matching `organizationId` appears pre-selected in the dropdown.
4. The author chooses a different organization and moves focus away from the picker.
5. The `onToggle` callback is invoked, allowing the parent form to update its state.

### No organization is pre-selected

1. The author opens a content form where no organization has been assigned (`organizationId` is absent or `null`).
2. The picker renders all available organizations in the dropdown.
3. The empty "None" option is shown as selected; no organization option is highlighted.

### Author belongs to no organizations

1. The author opens a content form but has no organization memberships.
2. The picker is rendered with an empty `organizations` array.
3. The dropdown contains only the "None" option and no organization entries.

### Accessibility compliance

1. The picker renders a `<select>` element with an accessible label (`aria-label="Select an organization"`).
2. The component passes automated accessibility checks with no violations.
