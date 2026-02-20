---
id: "01KHY7PZVZBXP0TEF480D3CB67"
name: "users_suggest_prominent_query"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/queries/users/suggest_prominent.rb
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
- spec/queries/users/suggest_prominent_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::SuggestProminent` within the users domain.

### Behavioral Areas

- **.call**: Ensures correct behavior under the specified conditions
- **when specifying attributes to select**: returns users with only specified attributes
- **with cached_followed_tags**: returns users with only specified attributes

### Implementation Architecture

The behavior is implemented across the following layers:

- **Query object**: `app/queries/users/suggest_prominent.rb` -- complex database query encapsulation
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

### S-1: does not include the calling user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not include the calling user

### S-2: returns users with only specified attributes

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns users with only specified attributes

### S-3: suggests users based on articles with matching tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** suggests users based on articles with matching tags

