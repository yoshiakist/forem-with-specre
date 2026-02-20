---
id: "01KHY7Q0PPSDX3DG7NQY76QQ0J"
name: "follows_create_api"
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
- spec/requests/follows_create_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Follows` within the follows domain.

### Behavioral Areas

- **Follows #create**: returns an error for too many follows in a day
- **when rate limit has been hit**: Ensures correct behavior under the specified conditions
- **when follows**: returns an error for too many follows in a day

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/api/v0/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/follows_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns an error for too many follows in a day

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an error for too many follows in a day

### S-2: returns followed

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns followed

### S-3: updates explicit points

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates explicit points

### S-4: unfollows

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** unfollows

