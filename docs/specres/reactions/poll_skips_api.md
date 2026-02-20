---
id: "01KHY7Q0FTQAMVB1FAK6WTYSV9"
name: "poll_skips_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/poll_skips_controller.rb
- spec/requests/poll_skips_spec.rb

## Functional Overview

This specification defines the expected behavior of `"PollSkips"` within the reactions domain.

### Behavioral Areas

- **PollSkips**: Ensures correct behavior under the specified conditions
- **POST /poll_skips**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/poll_skips_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: votes on behalf of current user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** votes on behalf of current user

### S-2: does not allow two skips

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow two skips

