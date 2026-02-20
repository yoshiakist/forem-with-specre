---
id: "01KHY7Q0HM2D3FS9CP5RFBGT1P"
name: "organization_policy_policy"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/policies/organization_policy.rb
- spec/policies/organization_policy_spec.rb

## Functional Overview

This specification defines the expected behavior of `OrganizationPolicy` within the organizations domain.

### Behavioral Areas

- **when user is not signed-in**: Ensures correct behavior under the specified conditions
- **when a non-org user**: Ensures correct behavior under the specified conditions
- **when user is suspended**: Ensures correct behavior under the specified conditions
- **when user is an org admin of an org**: Ensures correct behavior under the specified conditions
- **when user is a member of an org org**: Ensures correct behavior under the specified conditions
- **when user is an org admin of another org**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Policy layer**: `app/policies/organization_policy.rb` -- authorization and access control rules


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- forbid actions %i[update analytics]
- permit action create
- forbid actions %i[create update]
- permit actions %i[analytics update]
- permit actions %i[analytics]
- forbid actions %i[analytics update]

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

