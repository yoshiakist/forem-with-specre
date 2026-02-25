---
id: "01KJ7GD1GXR41KPP9FQDP5DGMY"
name: "admin_can_remove_role_from_user"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/users_controller.rb`
- `app/services/users/remove_role.rb`
- `app/policies/role_policy.rb`
- `app/models/role.rb`
- `app/views/admin/users/show/overview/_roles.html.erb` (Template)
- `spec/services/users/remove_role_spec.rb` (Test)
- `spec/policies/role_policy_spec.rb` (Test)

## Functional Overview

On the admin user detail page, each assigned role (except tag moderator roles, which are managed separately) is displayed as a pill. Whether the pill renders a remove button or a locked indicator depends on the current admin's authorization level: super admins may remove any role, while regular admins may remove any role except `super_admin`. When an admin clicks the remove button, a confirmation dialog is shown (with a special message for `super_admin` removal). The controller action looks up the `Role` record, authorizes the action via `RolePolicy#remove_role?`, then delegates to `Users::RemoveRole`, which attempts role removal with a resource context first and falls back to a resourceless removal; on completion it touches the user's profile to invalidate caches. The admin is redirected back to the user page with a localized success flash showing the role name, or a danger flash containing the error message on failure.

## Design Intent

The two-step removal in `Users::RemoveRole` (try with resource, then without) handles roles that may have been stored with or without a resource association, providing resilience against inconsistent data. Touching the user profile after role removal ensures that any cached profile headers reflect the updated role set immediately.

## Key Members

- `Users::RemoveRole::Response` — Struct with `success` (boolean) and `error_message` (string or nil) returned by the service.
- `role.name_labelize` — Resolves a human-friendly label for `single_resource_admin` roles scoped to a resource type; falls back to the raw role name for all other roles.

## Scenarios

### Removable role is displayed with a delete button

1. Admin visits the user detail page in the admin panel.
2. For each role where `RolePolicy#remove_role?` returns true, the view renders a pill with the role name and an X (delete) icon.
3. If the role is `super_admin`, the confirmation dialog uses a special warning message; otherwise a generic confirmation message is used.

### Non-removable role is displayed as locked

1. Admin visits the user detail page in the admin panel.
2. For each role where `RolePolicy#remove_role?` returns false (e.g., a regular admin viewing a `super_admin` role), the view renders a pill with a lock icon and a "locked" tooltip.
3. The pill is not interactive; no delete action is available.

### Admin successfully removes a role

1. Admin clicks the remove button on a role pill and confirms the dialog.
2. The browser sends a DELETE request including the role ID, user ID, and optional resource type/ID.
3. The controller finds the `Role` record and authorizes the action; authorization passes.
4. `Users::RemoveRole` removes the role (scoped by resource if applicable) and touches the user's profile.
5. A success flash message is shown with the localized role name and the admin is redirected to the user page.

### Authorization prevents unauthorized role removal

1. A regular admin attempts to remove the `super_admin` role from a user.
2. The controller calls `authorize(role, :remove_role?)`, which invokes `RolePolicy#remove_role?`.
3. Because the current user is not a super admin and the target role is `super_admin`, the policy returns false and an authorization error is raised.

## Failures / Exceptions

- If `Users::RemoveRole` raises a `StandardError` during role removal, the error is rescued, `response.success` remains false, and `response.error_message` is set to a localized error string. The controller then sets a danger flash with that message and redirects the admin back to the user page.
