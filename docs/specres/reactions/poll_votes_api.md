---
id: "01KHY7Q0G478RJRMV1KMVCBDHC"
name: "poll_votes_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/poll_votes_controller.rb
- spec/requests/poll_votes_spec.rb

## Functional Overview

This specification defines the expected behavior of `"PollVotes"` within the reactions domain.

### Behavioral Areas

- **PollVotes**: Ensures correct behavior under the specified conditions
- **GET /poll_votes/:id**: Ensures correct behavior under the specified conditions
- **POST /poll_votes**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/poll_votes_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns proper results for poll

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns proper results for poll

### S-2: returns proper results for poll if voted

- **Given** voted
- **When** the action is triggered
- **Then** returns proper results for poll

### S-3: creates a vote for the current user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a vote for the current user

### S-4: allows the current user to change their vote

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows the current user to change their vote

### S-5: does not create a duplicate vote if the same option is voted for twice

- **Given** the same option is voted for twice
- **When** the action is triggered
- **Then** does not create a duplicate vote

