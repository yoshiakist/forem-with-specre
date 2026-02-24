---
id: "01KJ7FGECMRSSPTAJBPC1KAZR8"
name: "admin_views_user_roles_on_profile"
status: "draft"
---

## Related Files

- `app/views/admin/users/show/overview/_roles.html.erb` (Template)

## Functional Overview

The roles partial on the admin user overview page displays all roles currently assigned to a given user, excluding tag moderator roles. When a user has no roles, an empty state message is shown alongside a button to open the role assignment modal. When roles are present, each role is rendered as a pill element. Roles that the current admin cannot remove are shown as locked, non-interactive pills with a tooltip explaining the restriction. Removable roles render as interactive pills with a delete button that posts a destroy request; removing a super admin role triggers a distinct confirmation dialog. An "Add role" button always appears at the bottom of the list to open the role assignment modal.

## Design Intent

Tag moderator roles are excluded from this list because they are managed through a separate surface (tag moderation settings), keeping this view focused on global and resource-scoped roles. Locked roles (e.g., the super admin's own role) are shown but made non-interactive to prevent accidental self-demotion while still communicating the full role set. A distinct confirmation message for super admin removal guards against high-impact accidents.

## Scenarios

### User has no roles assigned

1. Admin navigates to the user profile overview page.
2. The system finds no roles associated with the user.
3. The page displays an empty state message indicating no roles are assigned.
4. A button is shown allowing the admin to open the "Add role" modal.

### User has one or more removable roles

1. Admin navigates to the user profile overview page.
2. The system finds roles assigned to the user (tag moderator roles are excluded from display).
3. Each non-tag-moderator role is rendered as an interactive pill with the role name and a remove icon.
4. Admin clicks the remove button on a non-super-admin role and confirms the generic confirmation dialog.
5. The system submits a DELETE request for that role, and the role is removed from the user.

### Admin removes a super admin role

1. Admin navigates to the user profile overview page for a user with a super admin role.
2. The super admin role is rendered as a removable pill (assuming policy permits removal).
3. Admin clicks the remove button on the super admin role.
4. A distinct, more emphatic confirmation dialog is displayed warning about the action.
5. Admin confirms, and the system submits a DELETE request removing the super admin role.

### Role is locked (admin lacks permission to remove it)

1. Admin navigates to the user profile overview page.
2. A role exists for the user but the current admin's policy does not permit removal.
3. The role is rendered as a non-interactive pill with a lock icon and a "Locked" tooltip.
4. No remove button is present; the pill is marked as aria-disabled to communicate the restriction to assistive technology.

### Admin opens the role assignment modal

1. Admin clicks the "Add role" button (present whether the role list is empty or not).
2. The role assignment modal opens with the appropriate form action targeting the user's status endpoint.
3. Admin selects and assigns a new role via the modal form.
