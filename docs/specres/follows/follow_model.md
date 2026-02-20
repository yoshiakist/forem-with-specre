---
id: "01KHY7Q0NZJ6RXQQXTX0BTT7JA"
name: "follow_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/api/v0/followers_controller.rb
- app/controllers/api/v0/follows_controller.rb
- app/controllers/api/v1/followers_controller.rb
- app/controllers/api/v1/follows_controller.rb
- app/controllers/concerns/api/followers_controller.rb
- app/controllers/concerns/api/follows_controller.rb
- app/controllers/followings_controller.rb
- app/controllers/follows_controller.rb
- app/models/follow.rb
- app/policies/follow_policy.rb
- app/services/notifications/new_follower/follow_data.rb
- app/workers/notifications/new_follower_worker.rb
- app/workers/users/follow_worker.rb
- spec/models/follow_spec.rb

## Functional Overview

This specification defines the expected behavior of `Follow` within the follows domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **when enqueuing jobs**: Ensures correct behavior under the specified conditions
- **when creating and inline**: touches the follower user while creating
- **scopes**: Ensures correct behavior under the specified conditions
- **.non_suspended**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/api/v0/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/followings_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/follows_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/follow.rb` -- data persistence, validations, and associations
- **Policy layer**: `app/policies/follow_policy.rb` -- authorization and access control rules
- **Service layer**: `app/services/notifications/new_follower/follow_data.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/notifications/new_follower_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- validate inclusion of subscription status.in array %w[all articles none]
- validate presence of followable type
- validate presence of follower type
- validate presence of subscription status

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: follows user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** follows user

### S-3: calculates points with explicit and implicit combined

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calculates points with explicit and implicit combined

### S-4: enqueues send notification worker

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enqueues send notification worker

### S-5: does not enqueue send notification worker if user has no badge achievements

- **Given** user has no badge achievements
- **When** the action is triggered
- **Then** does not enqueue send notification worker

### S-6: touches the follower user while creating

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** touches the follower user while creating

### S-7: sends an email notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends an email notification

### S-8: excludes suspended users from the result

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** excludes suspended users from the result

### S-9: filters by followable type and id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** filters by followable type and id

### S-10: includes only Users in the result

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes only Users in the result

