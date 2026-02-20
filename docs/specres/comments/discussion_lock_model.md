---
id: "01KHY7PZP9140QR4Y46Q9XKBHA"
name: "discussion_lock_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/discussion_locks_controller.rb
- app/models/discussion_lock.rb
- app/policies/discussion_lock_policy.rb
- app/models/comment.rb
- app/models/concerns/algolia_searchable/searchable_comment.rb
- spec/models/discussion_lock_spec.rb

## Functional Overview

This specification defines the expected behavior of `DiscussionLock` within the comments domain.

### Behavioral Areas

- **relationships**: Ensures correct behavior under the specified conditions
- **validations**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/discussion_locks_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/discussion_lock.rb` -- data persistence, validations, and associations
- **Policy layer**: `app/policies/discussion_lock_policy.rb` -- authorization and access control rules
- **Model layer**: `app/models/comment.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_comment.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to article
- belong to locking user
- validate uniqueness of article id

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: sanitizes attributes before validation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sanitizes attributes before validation

