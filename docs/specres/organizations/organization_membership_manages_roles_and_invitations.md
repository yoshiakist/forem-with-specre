---
id: "01KHYABB1GB91QKA03127ZTDMJ"
name: "organization_membership_manages_roles_and_invitations"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/organization_membership.rb
- spec/models/organization_membership_spec.rb (Test)

## Functional Overview

The OrganizationMembership model manages the join relationship between User and Organization with role-based access control (admin, member, guest, pending), invitation token generation for pending members, cache invalidation on membership changes, and user timestamp updates for organization info freshness tracking.

## Scenarios

### Membership validates role and uniqueness

1. The system requires `type_of_user` to be present and one of: admin, member, guest, pending.
2. The system enforces that a user can have at most one membership per organization (unique user_id scoped to organization_id).

### Pending membership generates invitation token on create

1. When a membership is created with `type_of_user` set to "pending" and no existing invitation token, the system generates a URL-safe base64 token of 32 bytes.
2. If the membership already has an invitation token, the system preserves the existing token.
3. Non-pending memberships do not receive invitation tokens.

### Membership confirmation transitions pending to member

1. Calling `confirm!` on a pending membership updates `type_of_user` from "pending" to "member".

### Membership scopes filter by role

1. The `.pending` scope returns only memberships with type_of_user "pending".
2. The `.active` scope returns all memberships except those with type_of_user "pending".
3. The `.admin` scope returns only memberships with type_of_user "admin".
4. The `.member` scope returns memberships with type_of_user "admin" or "member".

### Membership triggers side effects on lifecycle events

1. After create and after destroy, the system touches the user's `organization_info_updated_at` timestamp.
2. After commit, the system enqueues `BustCachePathWorker` with the organization's path to invalidate cached pages.

## Key Members

- `type_of_user`: Role string — one of "admin", "member", "guest", "pending".
- `invitation_token`: URL-safe base64 token for pending invitation confirmation.
