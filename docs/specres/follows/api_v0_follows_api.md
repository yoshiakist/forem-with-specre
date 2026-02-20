---
id: "01KHY7Q0P6WWX8QMW23QYB2VHQ"
name: "api_v0_follows_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/api/v0/follows_controller.rb
- app/controllers/api/v1/follows_controller.rb
- app/controllers/concerns/api/follows_controller.rb
- app/controllers/follows_controller.rb
- app/controllers/api/v0/followers_controller.rb
- spec/requests/api/v0/follows_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Api::V0::FollowsController"` within the follows domain.

### Behavioral Areas

- **Api::V0::FollowsController**: Ensures correct behavior under the specified conditions
- **POST /api/follows**: Ensures correct behavior under the specified conditions
- **when user is authorized**: returns unauthorized if user is not signed in
- **GET /api/follows/tags**: Ensures correct behavior under the specified conditions
- **when user is authorized**: returns unauthorized if user is not signed in

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/api/v0/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/followers_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns unauthorized if user is not signed in

- **Given** user is not signed in
- **When** the action is triggered
- **Then** returns unauthorized

### S-2: returns the number of followed users

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the number of followed users

### S-3: creates follows

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates follows

### S-4: returns unauthorized if user is not signed in

- **Given** user is not signed in
- **When** the action is triggered
- **Then** returns unauthorized

### S-5: returns only the tags the user follows

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns only the tags the user follows

