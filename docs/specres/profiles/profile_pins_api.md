---
id: "01KHY7Q0KXG5J9MYPZB1XQW9C8"
name: "profile_pins_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/profile_pins_controller.rb
- spec/requests/profile_pins_spec.rb

## Functional Overview

This specification defines the expected behavior of `"ProfilePins"` within the profiles domain.

### Behavioral Areas

- **ProfilePins**: Ensures correct behavior under the specified conditions
- **POST /profile_pins**: Ensures correct behavior under the specified conditions
- **PUT /profile_pins/:id**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/profile_pins_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: creates a pin

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a pin

### S-2: allows only five pins

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows only five pins

### S-3: adds pin on behalf of current user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds pin on behalf of current user

