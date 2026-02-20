---
id: "01KHY7Q0PCS27CQTDR81BEBH55"
name: "api_v1_follows_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/api/v0/follows_controller.rb
- app/controllers/api/v1/follows_controller.rb
- app/controllers/concerns/api/follows_controller.rb
- app/controllers/follows_controller.rb
- app/controllers/api/v1/followers_controller.rb
- app/views/api/v1/follows/tags.json.jbuilder (Template)
- spec/requests/api/v1/follows_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Api::V1::FollowsController"` within the follows domain.

### Behavioral Areas

- **Api::V1::FollowsController**: Ensures correct behavior under the specified conditions
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
- **Controller layer**: `app/controllers/api/v1/followers_controller.rb` -- HTTP request routing and response handling


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

### S-4: can follow users or organizations

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** can follow users or organizations

### S-5: returns unauthorized if user is not signed in

- **Given** user is not signed in
- **When** the action is triggered
- **Then** returns unauthorized

### S-6: returns only the tags the user follows

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns only the tags the user follows

