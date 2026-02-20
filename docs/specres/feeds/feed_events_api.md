---
id: "01KHY7Q0Q6XZ41465B3AEES9QP"
name: "feed_events_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/feed_events_controller.rb
- spec/requests/feed_events_spec.rb

## Functional Overview

This specification defines the expected behavior of `"FeedEvents"` within the feeds domain.

### Behavioral Areas

- **FeedEvents**: Ensures correct behavior under the specified conditions
- **POST /feed_events**: Ensures correct behavior under the specified conditions
- **when user is signed in**: creates a feed click event when passed as header
- **when user is not signed in**: creates a feed click event when passed as header
- **when a token is provided**: creates a feed click event when passed as header

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/feed_events_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: creates a feed click event

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a feed click event

### S-2: creates a feed impression event

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a feed impression event

### S-3: creates multiple events in a batch

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates multiple events in a batch

### S-4: silently does not create an event

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** silently does not create an event

### S-5: creates a feed click event when passed as header

- **Given** the system is in a standard operational state
- **When** passed as header
- **Then** creates a feed click event

### S-6: creates a feed impression event when passed as param

- **Given** the system is in a standard operational state
- **When** passed as param
- **Then** creates a feed impression event

