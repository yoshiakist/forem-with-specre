---
id: "01KHY7PZE24EM7YX7Q65HZT1ZH"
name: "article_policy_policy"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/policies/article_policy.rb
- app/policies/pinned_article_policy.rb
- spec/policies/article_policy_spec.rb

## Functional Overview

This specification defines the expected behavior of `ArticlePolicy` within the articles domain.

### Behavioral Areas

- **.scope_users_authorized_to_action**: Ensures correct behavior under the specified conditions
- **when limit_post_creation_to_admins is true**: returns an empty result for create actions when no admins
- **when limit_post_creation_to_admins is false**: returns an empty result for create actions when no admins
- **when is_root_subforem? is true**: returns an empty result for create actions when no admins
- **.include_hidden_dom_class_for?**: Ensures correct behavior under the specified conditions
- **when limit_post_creation_to_admins is #{limit} and query is #{query}**: returns an empty result for create actions when no admins
- **when is_root_subforem? is true**: returns an empty result for create actions when no admins
- **and limit_post_creation_to_admins? is false**: returns false regardless of user role

### Implementation Architecture

The behavior is implemented across the following layers:

- **Policy layer**: `app/policies/article_policy.rb` -- authorization and access control rules
- **Policy layer**: `app/policies/pinned_article_policy.rb` -- authorization and access control rules


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- eq expected value
- be truthy
- be tag moderator eligible
- be tag moderator eligible
- be tag moderator eligible

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: omits suspended and regular users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** omits suspended and regular users

### S-3: omits only suspended users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** omits only suspended users

### S-4: returns users authorized to create in a root subforem

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns users authorized to create in a root subforem

### S-5: returns an empty result for create actions when no admins

- **Given** the system is in a standard operational state
- **When** no admins
- **Then** returns an empty result for create actions

### S-6: returns true to hide the DOM

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns true to hide the DOM

### S-7: still returns true to hide the DOM

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** still returns true to hide the DOM

### S-8: returns false regardless of user role

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns false regardless of user role

### S-9: is tag_moderator_eligible

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is tag_moderator_eligible

### S-10: is not tag_moderator_eligible

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is not tag_moderator_eligible

