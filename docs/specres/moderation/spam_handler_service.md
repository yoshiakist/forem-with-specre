---
id: "01KHY7Q0NC987TVHS844MRSF3F"
name: "spam_handler_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/spam/handler.rb
- app/services/notifications/remove_by_spammer.rb
- app/services/slack/messengers/potential_spammer.rb
- app/services/spam/domain_detector.rb
- app/services/spam/reaction_ring_detector.rb
- app/services/users/resolve_spam_reports.rb
- app/workers/articles/handle_spam_worker.rb
- app/workers/comments/handle_spam_worker.rb
- app/workers/notifications/remove_by_spammer_worker.rb
- app/workers/spam/block_domain_and_suspend_users_worker.rb
- app/workers/spam/reaction_ring_detection_worker.rb
- spec/services/spam/handler_spec.rb

## Functional Overview

This specification defines the expected behavior of `Spam::Handler` within the moderation domain.

### Behavioral Areas

- **.handle_article!**: Ensures correct behavior under the specified conditions
- **when content is not spam**: creates a reaction, notes, suspends, and unpublishes all posts when applicable
- **when spam is triggered by RateLimit**: creates a reaction, notes, suspends, and unpublishes all posts when applicable
- **for a first-time offender**: Ensures correct behavior under the specified conditions
- **for a multiple offender**: Ensures correct behavior under the specified conditions
- **when spam is triggered by AI check**: creates a reaction, notes, suspends, and unpublishes all posts when applicable
- **for a first-time offender**: Ensures correct behavior under the specified conditions
- **for a multiple offender**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/spam/handler.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/remove_by_spammer.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/slack/messengers/potential_spammer.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/spam/domain_detector.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/spam/reaction_ring_detector.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/resolve_spam_reports.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/articles/handle_spam_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/comments/handle_spam_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/notifications/remove_by_spammer_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/spam/block_domain_and_suspend_users_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/spam/reaction_ring_detection_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- eq not spam
- eq not spam
- eq not spam

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: creates a reaction but does not suspend the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a reaction but does not suspend the user

### S-3: creates a reaction, suspends the user, and creates a note for the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a reaction, suspends the user, and creates a note for the user

### S-4: creates a reaction, notes, suspends, and unpublishes all posts when applicable

- **Given** the system is in a standard operational state
- **When** applicable
- **Then** creates a reaction, notes, suspends, and unpublishes all posts

### S-5: creates a reaction but does not suspend the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a reaction but does not suspend the user

### S-6: returns :spam

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns :spam

### S-7: creates a reaction, suspends the user, and returns :spam

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a reaction, suspends the user, and returns :spam

### S-8: creates a reaction but does not suspend the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a reaction but does not suspend the user

### S-9: returns :spam

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns :spam

### S-10: bypasses badge count restrictions but still runs checks

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** bypasses badge count restrictions but still runs checks

### S-11: creates a reaction but does not suspend the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a reaction but does not suspend the user

### S-12: returns :spam

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns :spam

### S-13: bypasses badge count restrictions but still runs checks

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** bypasses badge count restrictions but still runs checks

