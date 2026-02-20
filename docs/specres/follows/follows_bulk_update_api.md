---
id: "01KHY7Q0PMYK51AGG13GGNZZ43"
name: "follows_bulk_update_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/api/v0/followers_controller.rb
- app/controllers/api/v0/follows_controller.rb
- app/controllers/api/v1/followers_controller.rb
- app/controllers/api/v1/follows_controller.rb
- app/controllers/concerns/api/followers_controller.rb
- app/controllers/concerns/api/follows_controller.rb
- spec/requests/follows_bulk_update_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Following/Unfollowing"` within the follows domain.

### Behavioral Areas

- **Following/Unfollowing**: Ensures correct behavior under the specified conditions
- **PATCH bulk_update**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/api/v0/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/follows_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: bulk updates follow explicit_points

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** bulk updates follow explicit_points

### S-2: does not update if follow does not belong to user

- **Given** follow does not belong to user
- **When** the action is triggered
- **Then** does not update

