---
id: "01KHY7Q1AQXZYGW2K27R7H6RWH"
name: "github_repo_policy_policy"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/policies/github_repo_policy.rb
- spec/policies/github_repo_policy_spec.rb

## Functional Overview

This specification defines the expected behavior of `GithubRepoPolicy` within the github_integration domain.

### Behavioral Areas

- **when user is not signed in**: Ensures correct behavior under the specified conditions
- **when the user is not authenticated through GitHub**: Ensures correct behavior under the specified conditions
- **when the user is authenticated through GitHub**: Ensures correct behavior under the specified conditions
- **when user is suspended**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Policy layer**: `app/policies/github_repo_policy.rb` -- authorization and access control rules


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- forbid actions %i[index update or create]
- permit actions %i[index update or create]
- forbid actions %i[index update or create]

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

