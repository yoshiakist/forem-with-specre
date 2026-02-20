---
id: "01KHY7Q0F7PZKNVGFP72H4RPVY"
name: "poll_vote_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/poll_votes_controller.rb
- app/models/poll_vote.rb
- app/models/poll_option.rb
- app/models/poll_skip.rb
- app/models/poll_text_response.rb
- app/models/privileged_reaction.rb
- app/models/rating_vote.rb
- app/models/reaction.rb
- app/models/reaction_category.rb
- spec/models/poll_vote_spec.rb

## Functional Overview

This specification defines the expected behavior of `PollVote` within the reactions domain.

### Behavioral Areas

- **when user has not voted nor skipped the poll**: allows only one vote per user per poll
- **validation rules for different poll types**: allows only one vote per user per poll
- **with single choice polls**: Ensures correct behavior under the specified conditions
- **with multiple choice polls**: allows multiple votes from the same user
- **with scale polls**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/poll_votes_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/poll_vote.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_option.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_skip.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_text_response.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/privileged_reaction.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/rating_vote.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/reaction.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/reaction_category.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: is not valid as a new object

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is not valid as a new object

### S-2: is valid

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is valid

### S-3: allows only one vote per user per poll

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows only one vote per user per poll

### S-4: allows multiple votes from the same user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows multiple votes from the same user

### S-5: prevents duplicate votes on the same option

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** prevents duplicate votes on the same option

### S-6: allows multiple votes from the same user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows multiple votes from the same user

### S-7: prevents duplicate votes on the same option

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** prevents duplicate votes on the same option

