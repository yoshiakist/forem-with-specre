---
id: "01KHY7PZZYB4YKNMSRWTTZR9H2"
name: "users_remove_role_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/users/remove_role.rb
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
- spec/services/users/remove_role_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::RemoveRole` within the users domain.

### Behavioral Areas

- **when removing tag mod role**: removes roles from users

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/users/remove_role.rb` -- business logic orchestration and domain operations
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

### S-1: removes roles from users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes roles from users

### S-2: removes :single_resource_admin roles from users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes :single_resource_admin roles from users

### S-3: removes the role (with resource_id)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes the role (with resource_id)

### S-4: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-5: returns an error if there is an issue removing the role

- **Given** there is an issue removing the role
- **When** the action is triggered
- **Then** returns an error

### S-6: touches users profile

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** touches users profile

