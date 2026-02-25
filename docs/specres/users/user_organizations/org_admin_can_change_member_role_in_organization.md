---
id: "01KJ9MY2XXBWSB527V49GHQ0KM"
name: "org_admin_can_change_member_role_in_organization"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/users_controller.rb`
- `spec/requests/user/user_organization_spec.rb` (Test)
- `app/views/users/_org_admin.html.erb` (Template)
- `app/views/users/_organization.html.erb` (Template)

## Functional Overview

An organization admin can manage the roles and membership of users within their organization. From the organization settings page, an org admin can promote an active member to admin status, revoke admin rights from another admin (downgrading them to member), remove any active member from the organization entirely, and cancel a pending invitation by removing the pending member. All three actions are POST requests handled by `UsersController` and require the current user to be an org admin of the target organization.

## Design Intent

These actions are intentionally restricted to user-facing org admins (via `current_user.org_admin?(org)` checks) rather than site-wide admins, keeping org membership self-governed. The controller uses `not_authorized` (Pundit) to gate access rather than a policy class, and the three actions are explicitly excluded from `verify_authorized` to avoid double-authorization. Each action redirects back to the organization settings page so the admin sees the updated member list immediately.

## Key Members

- `OrganizationMembership#type_of_user` — enum-like string field; `"admin"` or `"member"` for active users, `"pending"` for invited users not yet accepted
- `User#org_admin?(org)` — returns true when the user has an `OrganizationMembership` with `type_of_user == "admin"` for the given org
- `POST /users/add_org_admin` — promotes a member to admin; params: `user_id`, `organization_id`
- `POST /users/remove_org_admin` — downgrades an admin to member; params: `user_id`, `organization_id`
- `POST /users/remove_from_org` — removes any membership record; params: `user_id`, `organization_id`

## Scenarios

### Promoting a member to org admin

1. An org admin visits the organization settings page, which renders `_org_admin.html.erb` because their membership type is `"admin"`.
2. The active members list shows a "Make admin" button next to each member whose `type_of_user` is not `"admin"`.
3. The admin clicks "Make admin" and confirms the browser dialog.
4. The browser POSTs to `/users/add_org_admin` with the target `user_id` and `organization_id`.
5. The controller verifies the current user is an org admin and that the target user is already a member of the org; otherwise it raises `Pundit::NotAuthorizedError`.
6. The target user's `OrganizationMembership#type_of_user` is updated to `"admin"`.
7. The admin is redirected to the organization settings page with a success notice.

### Revoking admin rights from another org admin

1. An org admin visits the organization settings page.
2. The active members list shows a "Revoke admin" button next to each other admin (not next to the current user themselves).
3. The admin clicks "Revoke admin" and confirms the browser dialog.
4. The browser POSTs to `/users/remove_org_admin` with the target `user_id` and `organization_id`.
5. The controller verifies the current user is an org admin and that the target user is also currently an org admin; otherwise it raises `Pundit::NotAuthorizedError`.
6. The target user's `OrganizationMembership#type_of_user` is updated to `"member"`.
7. The admin is redirected to the organization settings page with a success notice.

### Removing an active member from the organization

1. An org admin visits the organization settings page.
2. The active members list shows a "Remove" button next to each non-admin member.
3. The admin clicks "Remove" and confirms the browser dialog.
4. The browser POSTs to `/users/remove_from_org` with the target `user_id` and `organization_id`.
5. The controller verifies the current user is an org admin and that an `OrganizationMembership` record exists for the target user; otherwise it raises `Pundit::NotAuthorizedError`.
6. The `OrganizationMembership` record is deleted (not just updated).
7. The admin is redirected to the organization settings page with a success notice.

### Cancelling a pending invitation

1. An org admin visits the organization settings page; the pending members section lists users who have been invited but have not yet accepted.
2. The admin clicks "Cancel invite" next to a pending member and confirms the browser dialog.
3. The browser POSTs to `/users/remove_from_org` with the pending user's `user_id` and `organization_id` (the same endpoint as removing an active member).
4. The controller verifies the current user is an org admin and that a membership record exists; otherwise it raises `Pundit::NotAuthorizedError`.
5. The pending `OrganizationMembership` record is deleted.
6. The admin is redirected to the organization settings page with a success notice.

## Failures / Exceptions

- If the current user is not an org admin of the specified organization, `not_authorized` is called, raising `Pundit::NotAuthorizedError` and returning a 403 response.
- For `add_org_admin`, if the target user is not already a member of the organization, `not_authorized` is also raised (the membership must pre-exist before it can be elevated).
- For `remove_org_admin`, if the target user is not currently an org admin, `not_authorized` is raised.
- An org admin cannot revoke their own admin status via these actions; the UI omits the "Revoke admin" button for the current user's own row.
