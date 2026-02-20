---
id: "01KHY7Q040TMKEJ8DMRAAFGFT8"
name: "moderator_banish_user_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/moderator/banish_user_worker.rb
- app/queries/users/select_moderators_query.rb
- app/services/moderator/banish_user.rb
- app/services/moderator/delete_user.rb
- app/services/moderator/merge_user.rb
- spec/workers/moderator/banish_user_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Moderator::BanishUserWorker` within the users domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/moderator/banish_user_worker.rb` -- asynchronous job processing
- **Query object**: `app/queries/users/select_moderators_query.rb` -- complex database query encapsulation
- **Service layer**: `app/services/moderator/banish_user.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/moderator/delete_user.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/moderator/merge_user.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: makes user suspended and username spam

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** makes user suspended and username spam

### S-2: deletes user content

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes user content

### S-3: reassigns profile info

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** reassigns profile info

### S-4: creates an entry in the BanishedUsers table

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an entry in the BanishedUsers table

### S-5: records who banished a user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** records who banished a user

