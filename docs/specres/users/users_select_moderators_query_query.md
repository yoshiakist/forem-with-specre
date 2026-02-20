---
id: "01KHY7PZVWABSW38V099V9BREN"
name: "users_select_moderators_query_query"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/queries/users/select_moderators_query.rb
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
- spec/queries/users/select_moderators_query_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::SelectModeratorsQuery` within the users domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Query object**: `app/queries/users/select_moderators_query.rb` -- complex database query encapsulation
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

### S-1: returns an accurate list of available moderators

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an accurate list of available moderators

### S-2: returns an empty array when there are no moderators that meet the criteria

- **Given** the system is in a standard operational state
- **When** there are no moderators that meet the criteria
- **Then** returns an empty array

