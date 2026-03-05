---
id: "01KHYACZKPN88W16YWM7C8YF7V"
name: "system_enforces_organization_authorization_policy"
status: "draft"
---

## Related Files

- `app/policies/organization_policy.rb`
- `spec/policies/organization_policy_spec.rb` (Test)

## Functional Overview

`OrganizationPolicy` defines Pundit-based authorization rules for all organization actions. It determines who may create, update, destroy, leave, and view analytics for an organization based on the current user's relationship to the organization. The policy delegates membership checks to convenience methods on the `User` model (`org_admin?`, `org_member?`, `spam_or_suspended?`). Secret regeneration uses the same rule as update, and analytics access uses the same rule as general membership.

## Key Members

- `OrganizationPolicy#create?` — permits any user who is not spam or suspended; does not require organization membership
- `OrganizationPolicy#update?` — permits only users who are admins of the target organization (`user.org_admin?(record)`)
- `OrganizationPolicy#destroy?` — permits super admins unconditionally, or org admins when the organization is `destroyable?`
- `OrganizationPolicy#leave_org?` — permits any user who is a member of the organization (any role including guest)
- `OrganizationPolicy#part_of_org?` — returns `true` if the user holds any membership in the organization; returns `false` if the record is blank
- `OrganizationPolicy#admin_of_org?` — returns `true` if the user is an admin of the organization; returns `false` if the record is blank
- `OrganizationPolicy#generate_new_secret?` — aliased to `update?`; requires org admin
- `OrganizationPolicy#analytics?` — aliased to `part_of_org?`; requires any membership

## Scenarios

### Non-suspended user creates an organization

1. An authenticated user who is not flagged as spam or suspended attempts to create an organization.
2. `create?` checks `!user.spam_or_suspended?` and returns `true`.
3. The action is authorized.

### Spam or suspended user attempts to create an organization

1. A user whose account is flagged as spam or suspended attempts to create an organization.
2. `create?` returns `false`.
3. Pundit raises `NotAuthorizedError` and the action is denied.

### Org admin updates or regenerates secret

1. An authenticated user who is an admin of the target organization attempts to update settings or regenerate the secret.
2. `update?` (or `generate_new_secret?`) checks `user.org_admin?(record)` and returns `true`.
3. The action is authorized.

### Non-admin member attempts to update

1. A user who is a member (but not an admin) of the organization attempts to update it.
2. `update?` returns `false` because the user is not an org admin.
3. The action is denied.

### Super admin destroys an organization

1. A super admin attempts to destroy any organization.
2. `destroy?` checks `user.super_admin?` first and returns `true` regardless of the organization's `destroyable?` status.

### Org admin destroys a destroyable organization

1. An org admin attempts to destroy an organization that has exactly one membership, zero articles, and zero credits.
2. `destroy?` checks `user.org_admin?(record) && record.destroyable?` and returns `true`.

### Org admin attempts to destroy a non-destroyable organization

1. An org admin attempts to destroy an organization that still has articles or credits.
2. `destroy?` returns `false` because `record.destroyable?` is `false`.
3. The action is denied.

### Member leaves an organization

1. A user who holds any role in the organization (admin, member, or guest) attempts to leave.
2. `leave_org?` delegates to `part_of_org?`, which checks `user.org_member?(record)` and returns `true`.
3. The action is authorized.

## Failures / Exceptions

- All policy checks return `false` rather than raising exceptions; Pundit's `authorize` call raises `Pundit::NotAuthorizedError` when a policy method returns `false`.
- `part_of_org?` and `admin_of_org?` guard against a blank record by returning `false` early, preventing `NoMethodError` on nil.
