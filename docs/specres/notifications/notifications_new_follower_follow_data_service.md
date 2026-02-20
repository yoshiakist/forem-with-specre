---
id: "01KHY7Q06Q7XGM5NDMH26BF38S"
name: "notifications_new_follower_follow_data_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/notifications/new_follower/follow_data.rb
- app/services/notifications/new_follower/send.rb
- app/workers/notifications/new_follower_worker.rb
- spec/services/notifications/new_follower/follow_data_spec.rb

## Functional Overview

This specification defines the expected behavior of `Notifications::NewFollower::FollowData` within the notifications domain.

### Behavioral Areas

- **.coerce**: Ensures correct behavior under the specified conditions
- **when given a Follow**: returns the given object
- **when given a Notifications::Reactions::ReactionData**: returns the given object
- **when given valid attributes**: returns the given object
- **when given invalid attributes**: returns the given object
- **to_h**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/notifications/new_follower/follow_data.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/new_follower/send.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/notifications/new_follower_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- be a described class
- be a described class

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: returns the given object

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the given object

### S-3: raises an DataError exception

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises an DataError exception

### S-4: returns a hash

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a hash

