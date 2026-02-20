---
id: "01KHY7Q04MP1S1GBNY5A7GSN4V"
name: "users_follow_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/users/follow_worker.rb
- app/controllers/admin/users_controller.rb
- app/controllers/api/v0/admin/users_controller.rb
- app/controllers/api/v0/users_controller.rb
- app/controllers/api/v1/admin/users_controller.rb
- app/controllers/api/v1/users_controller.rb
- app/controllers/concerns/api/admin/users_controller.rb
- app/controllers/concerns/api/users_controller.rb
- app/controllers/users/notification_settings_controller.rb
- app/controllers/users/settings_controller.rb
- app/controllers/users_controller.rb
- spec/workers/users/follow_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::FollowWorker` within the users domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **when followable doesn**: doesn
- **when user doesn**: doesn
- **when user + followable exist**: follows user

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/users/follow_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/notification_settings_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/settings_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-2: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-3: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-4: follows user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** follows user

