---
id: "01KHY7PZPFNN8MEZX1HTYCE1EW"
name: "discussion_lock_policy_policy"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/policies/discussion_lock_policy.rb
- app/policies/comment_policy.rb
- spec/policies/discussion_lock_policy_spec.rb

## Functional Overview

This specification defines the expected behavior of `DiscussionLockPolicy` within the comments domain.

### Behavioral Areas

- **when user is not signed-in**: Ensures correct behavior under the specified conditions
- **when user is not the author**: Ensures correct behavior under the specified conditions
- **when user is the author**: Ensures correct behavior under the specified conditions
- **when user is suspended**: Ensures correct behavior under the specified conditions
- **when user is an admin**: Ensures correct behavior under the specified conditions
- **when user is a super_admin**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Policy layer**: `app/policies/discussion_lock_policy.rb` -- authorization and access control rules
- **Policy layer**: `app/policies/comment_policy.rb` -- authorization and access control rules


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- forbid actions %i[create destroy]
- permit actions %i[create destroy]
- permit mass assignment of valid attributes
- forbid actions %i[create destroy]
- permit actions %i[create destroy]
- permit mass assignment of valid attributes
- permit actions %i[create destroy]
- permit mass assignment of valid attributes

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

