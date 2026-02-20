---
id: "01KHY7Q0NWXSMYBRYRZTJYF9D7"
name: "data_update_scripts_populate_explicit_follow_points_lib"
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
- spec/lib/data_update_scripts/populate_explicit_follow_points_spec.rb

## Functional Overview

This specification defines the expected behavior of `Populate_Explicit_Follow_Points` within the follows domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/api/v0/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/follows_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: updates follows that had points to having explicit points

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates follows that had points to having explicit points

