---
id: "01KHY7Q0G6ANNJ86DETCCGXKWH"
name: "rating_votes_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/rating_votes_controller.rb
- spec/requests/rating_votes_spec.rb

## Functional Overview

This specification defines the expected behavior of `"RatingVotes"` within the reactions domain.

### Behavioral Areas

- **RatingVotes**: Ensures correct behavior under the specified conditions
- **POST /rating_votes**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/rating_votes_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: creates a new rating vote

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new rating vote

### S-2: does not create new rating vote for non-trusted user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create new rating vote for non-trusted user

