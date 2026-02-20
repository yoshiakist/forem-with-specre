---
id: "01KHY7Q0FZK00VJH2D9HG81VWW"
name: "poll_text_responses_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/poll_text_responses_controller.rb
- spec/requests/poll_text_responses_spec.rb

## Functional Overview

This specification defines the expected behavior of `"PollTextResponses"` within the reactions domain.

### Behavioral Areas

- **PollTextResponses**: Ensures correct behavior under the specified conditions
- **POST /poll_text_responses**: Ensures correct behavior under the specified conditions
- **with valid parameters**: Ensures correct behavior under the specified conditions
- **with invalid parameters**: Ensures correct behavior under the specified conditions
- **when user is not authenticated**: creates a new text response when user submits again

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/poll_text_responses_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: creates a new text response

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new text response

### S-2: returns success even for empty text content (silent failure)

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns success even for empty text content (silent failure)

### S-3: returns success even for text content too long (silent failure)

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns success even for text content too long (silent failure)

### S-4: creates a new text response when user submits again

- **Given** the system is in a standard operational state
- **When** user submits again
- **Then** creates a new text response

### S-5: redirects to sign in

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to sign in

