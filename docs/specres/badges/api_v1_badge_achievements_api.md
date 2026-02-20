---
id: "01KHY7Q09PFR5SNT9FRGSC411Q"
name: "api_v1_badge_achievements_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/badge_achievements_controller.rb
- app/controllers/api/v0/badge_achievements_controller.rb
- app/controllers/api/v1/badge_achievements_controller.rb
- app/controllers/concerns/api/badge_achievements_controller.rb
- app/controllers/api/v1/badges_controller.rb
- spec/requests/api/v1/badge_achievements_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/api/badge_achievements"` within the badges domain.

### Behavioral Areas

- **/api/badge_achievements**: Ensures correct behavior under the specified conditions
- **GET /api/badge_achievements**: Ensures correct behavior under the specified conditions
- **GET /api/badge_achievements/:id**: Ensures correct behavior under the specified conditions
- **POST /api/badge_achievements**: Ensures correct behavior under the specified conditions
- **DELETE /api/badge_achievements/:id**: deletes the achievement

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/badge_achievements_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/badge_achievements_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/badge_achievements_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/badge_achievements_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/badges_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns a successful response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a successful response

### S-2: returns the specified achievement

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the specified achievement

### S-3: creates a new achievement with valid params and extra context

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new achievement with valid params and extra context

### S-4: does not create a duplicate achievement for a single-award badge

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create a duplicate achievement for a single-award badge

### S-5: deletes the achievement

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes the achievement

