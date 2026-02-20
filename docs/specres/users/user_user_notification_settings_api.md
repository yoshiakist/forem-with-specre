---
id: "01KHY7PZWTCS4W091TD95P6YBB"
name: "user_user_notification_settings_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/settings/user_experiences_controller.rb
- app/controllers/admin/user_queries_controller.rb
- app/controllers/admin/users_controller.rb
- app/controllers/api/v0/admin/users_controller.rb
- app/controllers/api/v0/users_controller.rb
- app/controllers/api/v1/admin/users_controller.rb
- app/controllers/api/v1/user_roles_controller.rb
- app/controllers/api/v1/users_controller.rb
- app/controllers/concerns/api/admin/users_controller.rb
- app/controllers/concerns/api/users_controller.rb
- spec/requests/user/user_notification_settings_spec.rb

## Functional Overview

This specification defines the expected behavior of `"UserNotificationSettings"` within the users domain.

### Behavioral Areas

- **UserNotificationSettings**: Ensures correct behavior under the specified conditions
- **PUT /update/:id**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/user_roles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: disables reaction notifications (in both users and notification_settings tables)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** disables reaction notifications (in both users and notification_settings tables)

### S-2: enables community-success notifications

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enables community-success notifications

### S-3: disables community-success notifications

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** disables community-success notifications

### S-4: can toggle welcome notifications

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** can toggle welcome notifications

