---
id: "01KHY7Q02ZN4D6XSC0GTXYYK9X"
name: "user_user_edits_profile_system"
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
- spec/system/user/user_edits_profile_spec.rb

## Functional Overview

This specification defines the expected behavior of `"User` within the users domain.

### Behavioral Areas

- **User edits their profile**: /settings/profile
- **visiting /settings/profile**: /settings/profile
- **editing admin created profile fields**: /settings/profile

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

### S-1: /settings/profile

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /settings/profile

### S-2: renders an error if the username contains spaces and thus is invalid

- **Given** the username contains spaces and thus is invalid
- **When** the action is triggered
- **Then** renders an error

### S-3: makes the 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** makes the 

### S-4: renders profile fields

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders profile fields

### S-5: reflects set profile fields in the interface

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** reflects set profile fields in the interface

### S-6: /#{user.username}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{user.username}

### S-7: respects static profile fields

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** respects static profile fields

### S-8: /#{user.username}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{user.username}

