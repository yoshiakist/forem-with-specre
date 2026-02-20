---
id: "01KHY7PZE5QMZ4RPEA3M7GWZ5S"
name: "pinned_article_policy_policy"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/policies/pinned_article_policy.rb
- app/policies/article_policy.rb
- spec/policies/pinned_article_policy_spec.rb

## Functional Overview

This specification defines the expected behavior of `PinnedArticlePolicy` within the articles domain.

### Behavioral Areas

- **when user is not signed in**: Ensures correct behavior under the specified conditions
- **when user is signed in as a regular user**: Ensures correct behavior under the specified conditions
- **when user is signed in as an admin**: Ensures correct behavior under the specified conditions
- **when user is signed in as a super_admin**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Policy layer**: `app/policies/pinned_article_policy.rb` -- authorization and access control rules
- **Policy layer**: `app/policies/article_policy.rb` -- authorization and access control rules


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- forbid actions %i[show update destroy]
- permit actions %i[show update destroy]
- permit actions %i[show update destroy]

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

