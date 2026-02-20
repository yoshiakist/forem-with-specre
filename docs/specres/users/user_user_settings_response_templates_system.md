---
id: "01KHY7Q034QEB5KC60T45P8HQD"
name: "user_user_settings_response_templates_system"
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
- spec/system/user/user_settings_response_templates_spec.rb

## Functional Overview

This specification defines the expected behavior of `"User` within the users domain.

### Behavioral Areas

- **User uses response templates settings**: can go to the edit page of the response template
- **when user is signed in**: shows the proper message when deleting a response template
- **when user has a response template already**: can go to the edit page of the response template

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

### S-1: can go to the edit page of the response template

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** can go to the edit page of the response template

### S-2: /settings/response-templates

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /settings/response-templates

### S-3: shows the proper message when deleting a response template

- **Given** the system is in a standard operational state
- **When** deleting a response template
- **Then** shows the proper message

### S-4: /settings/extensions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /settings/extensions

