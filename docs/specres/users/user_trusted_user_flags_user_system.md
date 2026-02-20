---
id: "01KHY7Q02QRQTZV5V6053R09PF"
name: "user_trusted_user_flags_user_system"
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
- spec/system/user/trusted_user_flags_user_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Flagging` within the users domain.

### Behavioral Areas

- **Flagging users from profile pages**: does not show a button for flagging yourself
- **when not logged in**: Ensures correct behavior under the specified conditions
- **when signed in as a non-trusted user**: Ensures correct behavior under the specified conditions
- **when signed in as the user**: Ensures correct behavior under the specified conditions
- **when signed in as a trusted user**: Ensures correct behavior under the specified conditions

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

### S-1: does not show the flag button

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not show the flag button

### S-2: does not show the flag button

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not show the flag button

### S-3: does not show a button for flagging yourself

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not show a button for flagging yourself

### S-4: allows toggling the flagged status

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows toggling the flagged status

