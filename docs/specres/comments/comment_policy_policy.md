---
id: "01KHY7PZPC4AZ2KD4M2JEBJV5M"
name: "comment_policy_policy"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/policies/comment_policy.rb
- app/policies/discussion_lock_policy.rb
- spec/policies/comment_policy_spec.rb

## Functional Overview

This specification defines the expected behavior of `CommentPolicy` within the comments domain.

### Behavioral Areas

- **when user is not signed-in**: Ensures correct behavior under the specified conditions
- **when user wants to subscribe to a comment**: Ensures correct behavior under the specified conditions
- **when user is not the author**: Ensures correct behavior under the specified conditions
- **with suspended status**: Ensures correct behavior under the specified conditions
- **with comment_suspended role**: Ensures correct behavior under the specified conditions
- **when user is a tag moderator**: Ensures correct behavior under the specified conditions
- **when user is an admin or super_admin**: Ensures correct behavior under the specified conditions
- **when user is trusted**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Policy layer**: `app/policies/comment_policy.rb` -- authorization and access control rules
- **Policy layer**: `app/policies/discussion_lock_policy.rb` -- authorization and access control rules


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- permit actions %i[subscribe]
- permit mass assignment of valid attributes for subscribe.for action subscribe
- permit actions %i[create]
- forbid actions %i[edit update destroy delete confirm hide unhide moderator create moderate]
- forbid actions %i[admin delete]
- permit mass assignment of valid attributes for create.for action create
- forbid actions %i[create edit update destroy delete confirm hide unhide admin delete]
- forbid actions %i[moderate]
- forbid actions %i[create edit update destroy delete confirm hide unhide admin delete]
- forbid actions %i[moderate]
- permit actions %i[create moderator create moderate]
- permit actions %i[create moderator create admin delete moderate]
- permit actions %i[moderator create]
- permit actions %i[edit update new create delete confirm destroy]
- forbid actions %i[moderator create admin delete moderate]

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

