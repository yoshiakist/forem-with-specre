---
id: "01KHY7Q0FM0VKX4RB5Q62EZC1W"
name: "reaction_policy_policy"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/policies/reaction_policy.rb
- app/policies/rating_vote_policy.rb
- spec/policies/reaction_policy_spec.rb

## Functional Overview

This specification defines the expected behavior of `ReactionPolicy` within the reactions domain.

### Behavioral Areas

- **.policy_query_for**: Ensures correct behavior under the specified conditions
- **when #{category} cateogry**: Ensures correct behavior under the specified conditions
- **when #{category} category**: Ensures correct behavior under the specified conditions
- **when nil category**: Ensures correct behavior under the specified conditions
- **when user is not signed in**: Ensures correct behavior under the specified conditions
- **when user is signed in**: Ensures correct behavior under the specified conditions
- **when user is suspended**: Ensures correct behavior under the specified conditions
- **when user is unadorned with roles**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Policy layer**: `app/policies/reaction_policy.rb` -- authorization and access control rules
- **Policy layer**: `app/policies/rating_vote_policy.rb` -- authorization and access control rules


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- eq privileged create?
- eq create?
- eq create?
- permit actions %i[index create]
- permit actions %i[index create]
- forbid actions %i[privileged create]
- permit actions %i[index create]
- forbid actions %i[privileged create]
- permit actions %i[index create privileged create]
- permit actions %i[index create privileged create]
- permit actions %i[index create privileged create]

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

