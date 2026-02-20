---
id: "01KHY7Q09VS0YTWWE45EEND670"
name: "badges_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/badges_controller.rb
- app/controllers/api/v0/badges_controller.rb
- app/controllers/api/v1/badges_controller.rb
- app/controllers/badges_controller.rb
- app/controllers/concerns/api/badges_controller.rb
- spec/requests/badges_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Badges"` within the badges domain.

### Behavioral Areas

- **Badges**: shows all the badges
- **GET /badges**: Ensures correct behavior under the specified conditions
- **when logged in**: Ensures correct behavior under the specified conditions
- **when logged out**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/badges_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: shows all the badges

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows all the badges

### S-2: shows all the badges

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows all the badges

