---
id: "01KHY7Q0G1V6REVGNX42JGPQXD"
name: "poll_votes_controller_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/poll_votes_controller.rb
- spec/requests/poll_votes_controller_spec.rb

## Functional Overview

This specification defines the expected behavior of `"PollVotesController"` within the reactions domain.

### Behavioral Areas

- **PollVotesController**: Ensures correct behavior under the specified conditions
- **GET /poll_votes/:id**: Ensures correct behavior under the specified conditions
- **when poll belongs to a survey**: returns poll voting data
- **POST /poll_votes**: Ensures correct behavior under the specified conditions
- **when poll belongs to a survey with resubmission allowed**: returns poll voting data
- **when poll belongs to a survey with resubmission not allowed**: returns poll voting data
- **when poll does not belong to a survey**: returns poll voting data

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/poll_votes_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns poll voting data

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns poll voting data

### S-2: creates a new vote with session_start

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new vote with session_start

### S-3: allows creating multiple votes for the same poll in different sessions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows creating multiple votes for the same poll in different sessions

### S-4: returns success but does not create a vote when survey is completed (silent fail...

- **Given** the system is in a standard operational state
- **When** survey is completed (silent failure)
- **Then** returns success but does not create a vote

### S-5: creates or updates vote using old behavior

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates or updates vote using old behavior

### S-6: updates existing vote for the same user and poll

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates existing vote for the same user and poll

