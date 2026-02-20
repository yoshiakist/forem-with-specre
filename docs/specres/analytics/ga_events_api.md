---
id: "01KHY7Q0Z3MPE526H0P6F8RB22"
name: "ga_events_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/ga_events_controller.rb
- spec/requests/ga_events_spec.rb

## Functional Overview

This specification defines the expected behavior of `"GaEvents"` within the analytics domain.

### Behavioral Areas

- **GaEvents**: Ensures correct behavior under the specified conditions
- **POST /fallback_activity_recorder**: posts to fallback_activity_recorder

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/ga_events_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: posts to fallback_activity_recorder

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** posts to fallback_activity_recorder

### S-2: renders normal response even if the Forem instance is private

- **Given** the Forem instance is private
- **When** the action is triggered
- **Then** renders normal response even

