---
id: "01KHY7Q0FWH7KB9DM2YDNQSJZZ"
name: "poll_text_responses_controller_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/poll_text_responses_controller.rb
- spec/requests/poll_text_responses_controller_spec.rb

## Functional Overview

This specification defines the expected behavior of `"PollText-responsesController"` within the reactions domain.

### Behavioral Areas

- **PollText-responsesController**: Ensures correct behavior under the specified conditions
- **POST /polls/:id/poll_text_responses**: Ensures correct behavior under the specified conditions
- **when poll belongs to a survey with resubmission allowed**: creates a new text response with session_start
- **when poll belongs to a survey with resubmission not allowed**: creates a new text response with session_start
- **when poll does not belong to a survey**: allows creating multiple responses for the same poll in different sessions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/poll_text_responses_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: creates a new text response with session_start

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new text response with session_start

### S-2: allows creating multiple responses for the same poll in different sessions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows creating multiple responses for the same poll in different sessions

### S-3: returns success but does not create a response when survey is completed (silent ...

- **Given** the system is in a standard operational state
- **When** survey is completed (silent failure)
- **Then** returns success but does not create a response

### S-4: creates or updates response using old behavior

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates or updates response using old behavior

### S-5: returns success but does not create a duplicate response (silent failure)

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns success but does not create a duplicate response (silent failure)

