---
id: "01KHY7Q0PHMJ421G6AJWYBRDSN"
name: "follows_bulk_show_api"
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
- spec/requests/follows_bulk_show_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Follows` within the follows domain.

### Behavioral Areas

- **Follows #bulk_show**: Ensures correct behavior under the specified conditions
- **when ids are present**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/api/v0/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/followers_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/follows_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns correct following values

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns correct following values

### S-2: without ids raises a missing param error

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** without ids raises a missing param error

### S-3: rejects unless logged-in

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects unless logged-in

