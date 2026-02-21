---
id: "01KJ02HFZZ1BJN4RQBAP4QA41P"
name: "user_can_leave_organization"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/users_controller.rb` (Controller — `leave_org` action)
- `app/policies/organization_policy.rb` (Policy — `leave_org?` authorization)
- `app/models/organization_membership.rb` (Model — membership record destroyed on leave)
- `app/views/users/_org_member.html.erb` (View — "Leave Organization" button form)
- `config/routes.rb` (Route — `POST users/leave_org/:organization_id`)
- `spec/system/organization/user_leaves_an_organization_spec.rb` (Test)

## Functional Overview

An authenticated user who is a member of an organization can leave that organization from their organization settings page. The settings page for a member organization shows a "Leave Organization" button. When the user clicks it, a browser confirmation dialog asks them to confirm the action. On confirmation, the system destroys the user's `OrganizationMembership` record, sets a flash notice, and redirects the user to the new organization settings page. The policy gate ensures only users who are currently part of the organization can perform this action.

## Design Intent

Leaving an organization is a destructive operation handled by a dedicated route and controller action rather than a generic `update` or `destroy` on an organization resource. This separation makes the intent explicit and keeps the authorization policy method (`leave_org?`) narrowly scoped: any current member can leave, but only admins can modify or delete the organization itself. The membership record's `after_destroy` callback keeps `organization_info_updated_at` fresh and busts the cache so stale member lists are not served.

## Key Members

- `OrganizationMembership` — the join record linking a user to an organization; destroying it removes the user from the organization.
- `type_of_user` — the role field on `OrganizationMembership`; valid values are `admin`, `member`, `guest`, and `pending`. Any active member may leave.
- `OrganizationPolicy#leave_org?` — returns `true` when the current user is a member (`org_member?`) of the target organization.
- Route `POST users/leave_org/:organization_id` (`users_leave_org_path`) — the named route submitted by the leave form.

## Scenarios

### User leaves a member organization

1. The signed-in user navigates to `/settings/organization/:id` for an organization they belong to.
2. The page renders the `_org_member` partial, which includes a "Leave Organization" button inside a form targeting `users_leave_org_path`.
3. The user clicks "Leave Organization"; a browser confirmation dialog is shown.
4. The user confirms; the browser submits a `POST` to `users/leave_org/:organization_id`.
5. `UsersController#leave_org` looks up the organization by `params[:organization_id]`.
6. The `OrganizationPolicy#leave_org?` check verifies the current user is a member; if not, an authorization error is raised.
7. The user's `OrganizationMembership` record is destroyed.
8. Destroying the membership triggers `update_user_organization_info_updated_at` (updates `organization_info_updated_at` on the user) and `bust_cache` (clears cached organization pages).
9. A flash notice "You have left your organization." is set.
10. The user is redirected to `/settings/organization/new`.

### Leave Organization button is visible to members

1. A signed-in user who is a member of an organization visits `/settings/organization/:id`.
2. The settings page renders the `_org_member` partial, which includes the "Leave Organization" button.

## Failures / Exceptions

- If the user is not a member of the specified organization, `OrganizationPolicy#leave_org?` returns `false` and the request is rejected with an authorization error (not authorized).
- If no `OrganizationMembership` record is found (e.g., already left), the safe-navigation operator (`&.destroy`) means the destroy is silently skipped; the flash notice and redirect still occur.
- If the user dismisses the browser confirmation dialog, the form is not submitted and the membership is not destroyed.
