---
id: "01KHY7Q0EZDY9RC2RAX6EJ2CDN"
name: "poll_option_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/poll_option.rb
- app/models/poll_skip.rb
- app/models/poll_text_response.rb
- app/models/poll_vote.rb
- app/models/privileged_reaction.rb
- app/models/rating_vote.rb
- app/models/reaction.rb
- app/models/reaction_category.rb
- spec/models/poll_option_spec.rb

## Functional Overview

This specification defines the expected behavior of `PollOption` within the reactions domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions
- **move_to_position**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/poll_option.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_skip.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_text_response.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_vote.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/privileged_reaction.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/rating_vote.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/reaction.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/reaction_category.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to poll
- have many poll votes.dependent destroy
- validate presence of markdown
- validate presence of poll votes count

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: allows up to 256 markdown characters

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows up to 256 markdown characters

### S-3: disallows over 256 markdown characters

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** disallows over 256 markdown characters

### S-4: allows up to 500 supplementary text characters

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows up to 500 supplementary text characters

### S-5: disallows over 500 supplementary text characters

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** disallows over 500 supplementary text characters

### S-6: moves option to new position and bumps others

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** moves option to new position and bumps others

### S-7: does nothing when moving to same position

- **Given** the system is in a standard operational state
- **When** moving to same position
- **Then** does nothing

