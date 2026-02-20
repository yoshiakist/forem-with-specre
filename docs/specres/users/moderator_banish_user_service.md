---
id: "01KHY7PZYDSQ16CRSQCDEZ9NK8"
name: "moderator_banish_user_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/moderator/banish_user.rb
- app/workers/moderator/banish_user_worker.rb
- app/queries/users/select_moderators_query.rb
- app/services/moderator/delete_user.rb
- app/services/moderator/merge_user.rb
- spec/services/moderator/banish_user_spec.rb

## Functional Overview

This specification defines the expected behavior of `Moderator::BanishUser` within the users domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/moderator/banish_user.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/moderator/banish_user_worker.rb` -- asynchronous job processing
- **Query object**: `app/queries/users/select_moderators_query.rb` -- complex database query encapsulation
- **Service layer**: `app/services/moderator/delete_user.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/moderator/merge_user.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: updates username, clears profile, and add BanishedUser record

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates username, clears profile, and add BanishedUser record

### S-2: removes everything

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes everything

