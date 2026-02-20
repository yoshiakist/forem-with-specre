---
id: "01KHY7Q03184HQSVWZMBJP46Z5"
name: "user_user_self_destroy_system"
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
- spec/system/user/user_self_destroy_spec.rb

## Functional Overview

This specification defines the expected behavior of `"User` within the users domain.

### Behavioral Areas

- **User destroys their profile**: displays a detailed error message when the user is not logged in

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

### S-1: requests self-destroy

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** requests self-destroy

### S-2: /settings/account

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /settings/account

### S-3: displays a detailed error message when the user is not logged in

- **Given** the system is in a standard operational state
- **When** the user is not logged in
- **Then** displays a detailed error message

### S-4: /users/confirm_destroy/#{token}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /users/confirm_destroy/#{token}

### S-5: displays a detailed error message when the user

- **Given** the system is in a standard operational state
- **When** the user
- **Then** displays a detailed error message

### S-6: /users/confirm_destroy/#{token}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /users/confirm_destroy/#{token}

### S-7: raises a 

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises a 

### S-8: /settings/account

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /settings/account

### S-9: destroys an account

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** destroys an account

### S-10: /users/confirm_destroy/#{token}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /users/confirm_destroy/#{token}

