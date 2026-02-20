---
id: "01KHY7PZVS44HVEM5QT3VXN6J9"
name: "user_policy_policy"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/policies/user_policy.rb
- app/policies/registration_policy.rb
- app/policies/user_block_policy.rb
- spec/policies/user_policy_spec.rb

## Functional Overview

This specification defines the expected behavior of `UserPolicy` within the users domain.

### Behavioral Areas

- **when user is not signed-in**: Ensures correct behavior under the specified conditions
- **when user is signed-in**: Ensures correct behavior under the specified conditions
- **with suspended status**: Ensures correct behavior under the specified conditions
- **when user is trusted**: Ensures correct behavior under the specified conditions
- **when user is not trusted**: Ensures correct behavior under the specified conditions
- **when the user is an admin**: Ensures correct behavior under the specified conditions
- **when the user is a super admin**: Ensures correct behavior under the specified conditions
- **when the user is a moderator**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Policy layer**: `app/policies/user_policy.rb` -- authorization and access control rules
- **Policy layer**: `app/policies/registration_policy.rb` -- authorization and access control rules
- **Policy layer**: `app/policies/user_block_policy.rb` -- authorization and access control rules


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- permit actions permitted actions
- forbid actions %i[join org moderation routes update]
- permit actions %i[moderation routes]
- forbid actions %i[moderation routes]
- permit actions %i[moderation routes]
- permit actions %i[moderation routes]
- permit actions %i[moderation routes]

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

