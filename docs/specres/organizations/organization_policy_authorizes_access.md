---
id: "01KHYACZKPN88W16YWM7C8YF7V"
name: "organization_policy_authorizes_access"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/policies/organization_policy.rb
- spec/policies/organization_policy_spec.rb (Test)

## Functional Overview

The OrganizationPolicy implements Pundit-based authorization rules for organization actions, controlling who can create, update, destroy, and access analytics for an organization based on user roles (org admin, org member, super admin) and user status (suspended/spam).

## Scenarios

### Unauthenticated user is rejected

1. When no user is signed in, all policy checks raise `Pundit::NotAuthorizedError`.

### Non-org user can only create organizations

1. A regular user who is not a member of the organization is permitted to create a new organization.
2. A regular user who is not a member is forbidden from updating or viewing analytics.

### Suspended or spam user cannot create organizations

1. If the user is suspended or flagged as spam, the system forbids the create action.

### Org admin can update and view analytics

1. An org admin of the specific organization is permitted to update the organization and view analytics.
2. The `generate_new_secret?` permission follows the same rules as update (aliased).

### Org member can view analytics but not update

1. An org member (non-admin) is permitted to view analytics for their organization.
2. An org member is forbidden from updating the organization.

### Org admin of a different org has no access

1. Being an admin of a different organization does not grant update or analytics permissions on another organization.

### Destroy requires super admin or admin of destroyable org

1. A super admin can destroy any organization.
2. An org admin can destroy their organization only if it is in a destroyable state (one membership, zero articles, zero credits).
