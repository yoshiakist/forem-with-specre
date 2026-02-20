---
id: "01KHY7Q003KZDMM635N2M8TCAN"
name: "users_suggest_for_sidebar_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/users/suggest_for_sidebar.rb
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
- spec/services/users/suggest_for_sidebar_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::SuggestForSidebar` within the users domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/users/suggest_for_sidebar.rb` -- business logic orchestration and domain operations
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

### S-1: returns user suggestions

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns user suggestions

### S-2: returns no user if there

- **Given** there
- **When** the action is triggered
- **Then** returns no user

### S-3: returns no user if not signed in

- **Given** not signed in
- **When** the action is triggered
- **Then** returns no user

