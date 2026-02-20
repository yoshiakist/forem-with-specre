---
id: "01KHY7Q0GQDH1D7GG50FCR0R5V"
name: "rating_votes_assign_rating_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/rating_votes/assign_rating_worker.rb
- app/controllers/rating_votes_controller.rb
- spec/workers/rating_votes/assign_rating_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `RatingVotes::AssignRatingWorker` within the reactions domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/rating_votes/assign_rating_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/rating_votes_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: assigns explicit score

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** assigns explicit score

### S-2: assigns implicit readinglist_reaction score

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** assigns implicit readinglist_reaction score

### S-3: assigns implicit comment score

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** assigns implicit comment score

