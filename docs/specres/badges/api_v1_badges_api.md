---
id: "01KHY7Q09SNGZ68ETRZPVW1GKJ"
name: "api_v1_badges_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/badges_controller.rb
- app/controllers/api/v0/badges_controller.rb
- app/controllers/api/v1/badges_controller.rb
- app/controllers/badges_controller.rb
- app/controllers/concerns/api/badges_controller.rb
- app/controllers/api/v1/badge_achievements_controller.rb
- spec/requests/api/v1/badges_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/api/badges"` within the badges domain.

### Behavioral Areas

- **/api/badges**: Ensures correct behavior under the specified conditions
- **GET /api/badges**: Ensures correct behavior under the specified conditions
- **when unauthorized (not an admin)**: Ensures correct behavior under the specified conditions
- **when authorized (as an admin)**: Ensures correct behavior under the specified conditions
- **GET /api/badges/:id**: Ensures correct behavior under the specified conditions
- **when authorized (as an admin)**: Ensures correct behavior under the specified conditions
- **POST /api/badges**: Ensures correct behavior under the specified conditions
- **when authorized (as an admin)**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/badge_achievements_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: rejects requests from regular users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects requests from regular users

### S-2: returns a paginated list of 50 badges

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a paginated list of 50 badges

### S-3: returns the specified badge

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the specified badge

### S-4: creates a new badge with valid params

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new badge with valid params

### S-5: updates the badge with valid params

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the badge with valid params

### S-6: does not update the badge with invalid params

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not update the badge with invalid params

### S-7: rejects the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects the request

### S-8: deletes the badge

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes the badge

