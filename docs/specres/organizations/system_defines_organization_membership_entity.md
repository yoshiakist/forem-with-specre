---
id: "01KHYABB1GB91QKA03127ZTDMJ"
name: "system_defines_organization_membership_entity"
status: "draft"
---

## Related Files

- `app/models/organization_membership.rb`
- `spec/models/organization_membership_spec.rb` (Test)

## Functional Overview

The `OrganizationMembership` model represents the link between a user and an organization, tracking the user's role and invitation state. Each membership has a `type_of_user` field constrained to one of four values: `"admin"`, `"member"`, `"guest"`, or `"pending"`. A user may belong to a given organization at most once (enforced by a uniqueness constraint on the `user_id`/`organization_id` pair). Pending memberships carry an auto-generated `invitation_token` for email-based confirmation. The model touches the user's `organization_info_updated_at` timestamp on create and destroy to signal downstream caches, and busts the organization page cache on any commit.

## Key Members

- `OrganizationMembership#type_of_user` — one of `"admin"`, `"member"`, `"guest"`, `"pending"`; validated for presence and inclusion in `USER_TYPES`
- `OrganizationMembership#invitation_token` — URL-safe random token generated before creation when `type_of_user` is `"pending"` and token is blank; used as the confirmation URL parameter
- `OrganizationMembership#pending?` — returns `true` when `type_of_user == "pending"`
- `OrganizationMembership#confirm!` — transitions `type_of_user` from `"pending"` to `"member"` via `update!`
- Scopes: `.admin` (type_of_user = admin), `.member` (admin or member), `.pending` (pending), `.active` (not pending)

## Scenarios

### Membership is created for an active user

1. A caller creates an `OrganizationMembership` with `type_of_user` set to `"admin"` or `"member"`.
2. The `user_id`/`organization_id` uniqueness validation passes.
3. No invitation token is generated because the type is not `"pending"`.
4. After create, `update_user_organization_info_updated_at` touches the user's `organization_info_updated_at` timestamp.
5. After commit, `bust_cache` enqueues `BustCachePathWorker` for the organization's path.

### Pending membership is created (invitation flow)

1. A caller creates an `OrganizationMembership` with `type_of_user: "pending"` and no `invitation_token`.
2. Before create, `generate_invitation_token` generates a 32-byte URL-safe base64 token and assigns it to `invitation_token`.
3. The record is saved with the generated token.
4. After create callbacks fire as above (user timestamp touch, cache bust).

### Pending membership is confirmed

1. A caller invokes `confirm!` on a pending membership.
2. The method calls `update!(type_of_user: "member")`, transitioning the membership to active.
3. After commit, cache busting is triggered.

### Membership is destroyed

1. A caller destroys an `OrganizationMembership` record.
2. After destroy, `update_user_organization_info_updated_at` touches the user's timestamp.
3. After commit, cache busting is triggered for the organization's path.

## Failures / Exceptions

- If a user already has a membership in the same organization, the uniqueness validation on `[user_id, organization_id]` fails and the record is not saved.
- If `type_of_user` is blank or not in `USER_TYPES`, the inclusion/presence validation fails.
- When the associated user is destroyed with `dependent: :delete_all`, no before/after destroy callbacks run on the membership (as noted in the model).
