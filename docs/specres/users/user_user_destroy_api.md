---
id: "01KHY7PZWQNRDGMH89ZXCXC46W"
name: "user_user_destroy_api"
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
- spec/requests/user/user_destroy_spec.rb

## Functional Overview

This specification defines the expected behavior of `"UserDestroy"` within the users domain.

### Behavioral Areas

- **UserDestroy**: Ensures correct behavior under the specified conditions
- **GET /settings/account**: Ensures correct behavior under the specified conditions
- **DELETE /users/full_delete**: offers to delete account when user has an email
- **when user has an email**: offers to delete account when user has an email
- **when user doesn**: offers to delete account when user has an email
- **POST /users/request_destroy**: Ensures correct behavior under the specified conditions
- **when user has an email**: offers to delete account when user has an email
- **when user doesn**: offers to delete account when user has an email

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

### S-1: offers to delete account when user has an email

- **Given** the system is in a standard operational state
- **When** user has an email
- **Then** offers to delete account

### S-2: offers to set an email when user doesn

- **Given** the system is in a standard operational state
- **When** user doesn
- **Then** offers to set an email

### S-3: schedules a user delete job

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** schedules a user delete job

### S-4: signs out

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** signs out

### S-5: redirects to sign up

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to sign up

### S-6: redirects to account page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to account page

### S-7: sends an email

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends an email

### S-8: updates the destroy_token in cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the destroy_token in cache

### S-9: sets flash notice

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets flash notice

### S-10: redirects to account page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to account page

### S-11: does not send an email if already requested

- **Given** already requested
- **When** the action is triggered
- **Then** does not send an email

### S-12: displays a flash message if user doesn

- **Given** user doesn
- **When** the action is triggered
- **Then** displays a flash message

