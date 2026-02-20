---
id: "01KHY7Q0FCNB5MZA604ZQ5R1SQ"
name: "reaction_category_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/reaction_category.rb
- app/models/poll_option.rb
- app/models/poll_skip.rb
- app/models/poll_text_response.rb
- app/models/poll_vote.rb
- app/models/privileged_reaction.rb
- app/models/rating_vote.rb
- app/models/reaction.rb
- spec/models/reaction_category_spec.rb

## Functional Overview

This specification defines the expected behavior of `ReactionCategory` within the reactions domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/reaction_category.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_option.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_skip.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_text_response.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_vote.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/privileged_reaction.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/rating_vote.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/reaction.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: returns category object via [:slug]

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns category object via [:slug]

### S-2: lists all category slugs

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** lists all category slugs

### S-3: lists public categories

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** lists public categories

### S-4: lists privileged categories

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** lists privileged categories

### S-5: lists negative_privileged categories

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** lists negative_privileged categories

### S-6: initializes via an attributes hash

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** initializes via an attributes hash

### S-7: name defaults to Slug

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** name defaults to Slug

### S-8: score defaults to 1.0

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** score defaults to 1.0

### S-9: privileged defaults to false

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** privileged defaults to false

### S-10: published defaults to true

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** published defaults to true

### S-11: position defaults to 99

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** position defaults to 99

### S-12: is positive when score is above zero

- **Given** the system is in a standard operational state
- **When** score is above zero
- **Then** is positive

