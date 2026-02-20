---
id: "01KHY7Q0FEG4VAX77YNZKA5YX8"
name: "reaction_ring_detection_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/spam/reaction_ring_detection_worker.rb
- app/models/poll_option.rb
- app/models/poll_skip.rb
- app/models/poll_text_response.rb
- app/models/poll_vote.rb
- app/models/privileged_reaction.rb
- app/models/rating_vote.rb
- app/models/reaction.rb
- app/models/reaction_category.rb
- spec/models/reaction_ring_detection_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Reaction` within the reactions domain.

### Behavioral Areas

- **Reaction ring detection**: does not trigger ring detection
- **check_for_reaction_ring callback**: Ensures correct behavior under the specified conditions
- **when reaction is not public**: Ensures correct behavior under the specified conditions
- **when reaction is not on an article**: Ensures correct behavior under the specified conditions
- **when user has insufficient reactions**: Ensures correct behavior under the specified conditions
- **when user has sufficient reactions and creates a public reaction on article**: Ensures correct behavior under the specified conditions
- **when user creates a public reaction**: Ensures correct behavior under the specified conditions
- **when user has old reactions outside 3-month window**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/spam/reaction_ring_detection_worker.rb` -- asynchronous job processing
- **Model layer**: `app/models/poll_option.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_skip.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_text_response.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_vote.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/privileged_reaction.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/rating_vote.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/reaction.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/reaction_category.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: does not trigger ring detection

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not trigger ring detection

### S-2: does not trigger ring detection

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not trigger ring detection

### S-3: does not trigger ring detection

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not trigger ring detection

### S-4: triggers ring detection

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** triggers ring detection

### S-5: triggers ring detection

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** triggers ring detection

### S-6: does not trigger ring detection

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not trigger ring detection

