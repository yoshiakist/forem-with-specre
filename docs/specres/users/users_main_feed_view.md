---
id: "01KHY7Q03RQ4BXYT8553HRF98S"
name: "users_main_feed_view"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

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
- spec/views/users/main_feed_spec.rb

## Functional Overview

This specification defines the expected behavior of `"users/show"` within the users domain.

### Behavioral Areas

- **users/show**: Ensures correct behavior under the specified conditions
- **when signed-in**: Ensures correct behavior under the specified conditions
- **when there are posts**: Ensures correct behavior under the specified conditions
- **when there are comments**: renders comments as required
- **when there are pinned stories**: renders no featured stories
- **when there are posts**: Ensures correct behavior under the specified conditions
- **when there are comments**: renders comments as required
- **when there are pinned stories**: renders no featured stories

### Implementation Architecture

The behavior is implemented across the following layers:

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

### S-1: renders no featured stories

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders no featured stories

### S-2: renders comments as required

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders comments as required

### S-3: renders no featured stories

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders no featured stories

### S-4: does not render comments, but sign-in CTA

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not render comments, but sign-in CTA

### S-5: renders without exception

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders without exception

