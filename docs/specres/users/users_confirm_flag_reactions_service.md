---
id: "01KHY7PZZM6KDSTK6HH5CCK2M6"
name: "users_confirm_flag_reactions_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/users/confirm_flag_reactions.rb
- app/workers/users/confirm_flag_reactions_worker.rb
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
- spec/services/users/confirm_flag_reactions_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::ConfirmFlagReactions` within the users domain.

### Behavioral Areas

- **with flag reactions**: updates statuses of the flag reactions to user, articles and comments

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/users/confirm_flag_reactions.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/users/confirm_flag_reactions_worker.rb` -- asynchronous job processing
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

### S-1: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-2: updates statuses of the flag reactions to user, articles and comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates statuses of the flag reactions to user, articles and comments

### S-3: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-4: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

