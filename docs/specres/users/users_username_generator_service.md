---
id: "01KHY7Q00937DP5WAKAXARF0N0"
name: "users_username_generator_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/users/username_generator.rb
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
- spec/services/users/username_generator_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::UsernameGenerator` within the users domain.

### Behavioral Areas

- **when username already exists**: returns randomly generated username if empty list is passed
- **when all generation methods are exhausted**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/users/username_generator.rb` -- business logic orchestration and domain operations
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

### S-1: returns randomly generated username if empty list is passed

- **Given** empty list is passed
- **When** the action is triggered
- **Then** returns randomly generated username

### S-2: returns randomly generated username if bad list is passed

- **Given** bad list is passed
- **When** the action is triggered
- **Then** returns randomly generated username

### S-3: returns supplied username if does not exist

- **Given** does not exist
- **When** the action is triggered
- **Then** returns supplied username

### S-4: returns normalized username

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns normalized username

### S-5: returns supplied username with suffix

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns supplied username with suffix

### S-6: returns nil

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns nil

