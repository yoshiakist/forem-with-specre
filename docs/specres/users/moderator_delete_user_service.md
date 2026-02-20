---
id: "01KHY7PZYF7JK25QXJ3Q2FG6AX"
name: "moderator_delete_user_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/moderator/delete_user.rb
- app/queries/users/select_moderators_query.rb
- app/services/moderator/banish_user.rb
- app/services/moderator/merge_user.rb
- app/workers/moderator/banish_user_worker.rb
- spec/services/moderator/delete_user_spec.rb

## Functional Overview

This specification defines the expected behavior of `Moderator::DeleteUser` within the users domain.

### Behavioral Areas

- **delete_user**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/moderator/delete_user.rb` -- business logic orchestration and domain operations
- **Query object**: `app/queries/users/select_moderators_query.rb` -- complex database query encapsulation
- **Service layer**: `app/services/moderator/banish_user.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/moderator/merge_user.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/moderator/banish_user_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: deletes user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes user

### S-2: deletes user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes user

### S-3: deletes user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes user

