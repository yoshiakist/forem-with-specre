---
id: "01KHY7Q0P4DGSD809S8JVPZ3ZE"
name: "api_v0_followers_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/api/v0/followers_controller.rb
- app/controllers/api/v1/followers_controller.rb
- app/controllers/concerns/api/followers_controller.rb
- app/controllers/api/v0/follows_controller.rb
- spec/requests/api/v0/followers_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Api::V0::FollowersController"` within the follows domain.

### Behavioral Areas

- **Api::V0::FollowersController**: Ensures correct behavior under the specified conditions
- **GET /api/followers/users**: Ensures correct behavior under the specified conditions
- **when user is unauthorized**: returns unauthorized
- **when the user is authorized as current_user**: returns unauthorized
- **when user is authorized with api key**: returns unauthorized

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/api/v0/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/follows_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns unauthorized

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns unauthorized

### S-2: returns ok

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns ok

### S-3: returns user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns user

### S-4: supports pagination

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** supports pagination

### S-5: orders results by descending following date by default

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** orders results by descending following date by default

### S-6: orders results by ascending following date if the 

- **Given** the
- **When** the action is triggered
- **Then** orders results by ascending following date

