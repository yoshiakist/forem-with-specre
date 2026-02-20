---
id: "01KHY7Q036FJAKKN12ARY9A93P"
name: "user_view_user_index_system"
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
- spec/system/user/view_user_index_spec.rb

## Functional Overview

This specification defines the expected behavior of `"User` within the users domain.

### Behavioral Areas

- **User index**: /#{user.username}
- **when user is unauthorized**: /#{user.username}
- **when 1 article**: shows articles
- **when user has an organization membership**: /#{user.username}
- **when user is logged in**: /#{user.username}
- **when user visits a profile**: /#{user.username}
- **when visiting own profile**: Ensures correct behavior under the specified conditions
- **when user is logged in**: /#{user.username}

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

### S-1: /#{user.username}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{user.username}

### S-2: shows header

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows header

### S-3: shows title

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows title

### S-4: shows articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows articles

### S-5: shows comments locked cta

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows comments locked cta

### S-6: hides comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** hides comments

### S-7: /#{user.username}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{user.username}

### S-8: shows organizations

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows organizations

### S-9: /#{user.username}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{user.username}

### S-10: shows_comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows_comments

### S-11: shows comment timestamp

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows comment timestamp

### S-12: /#{user.username}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{user.username}

