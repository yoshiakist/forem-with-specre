---
id: "01KHY7PZZQ0JDZ587JMHWMAZFV"
name: "users_create_mascot_account_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/users/create_mascot_account.rb
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
- spec/services/users/create_mascot_account_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::CreateMascotAccount` within the users domain.

### Behavioral Areas

- **when a mascot user doesn**: defines MASCOT_PARMS
- **when a mascot user already exists**: defines MASCOT_PARMS

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/users/create_mascot_account.rb` -- business logic orchestration and domain operations
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

### S-1: defines MASCOT_PARMS

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** defines MASCOT_PARMS

### S-2: creates a mascot account

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a mascot account

### S-3: raises an error

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises an error

