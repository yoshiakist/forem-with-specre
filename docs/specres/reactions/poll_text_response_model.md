---
id: "01KHY7Q0F4743CZXH69Y7KRFXE"
name: "poll_text_response_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/poll_text_responses_controller.rb
- app/models/poll_text_response.rb
- app/models/poll_option.rb
- app/models/poll_skip.rb
- app/models/poll_vote.rb
- app/models/privileged_reaction.rb
- app/models/rating_vote.rb
- app/models/reaction.rb
- app/models/reaction_category.rb
- spec/models/poll_text_response_spec.rb

## Functional Overview

This specification defines the expected behavior of `PollTextResponse` within the reactions domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **associations**: Ensures correct behavior under the specified conditions
- **valid text response**: is valid with valid attributes
- **invalid text response**: is invalid without text content

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/poll_text_responses_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/poll_text_response.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_option.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_skip.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_vote.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/privileged_reaction.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/rating_vote.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/reaction.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/reaction_category.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- validate presence of text content
- validate length of text content.is at most 1000
- validate uniqueness of poll id.scoped to user id, :session start
- belong to poll
- belong to user

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: is valid with valid attributes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is valid with valid attributes

### S-3: is invalid without text content

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is invalid without text content

### S-4: is invalid with text content longer than 1000 characters

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is invalid with text content longer than 1000 characters

### S-5: prevents duplicate responses from the same user for the same poll in the same se...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** prevents duplicate responses from the same user for the same poll in the same session

### S-6: allows responses from the same user for the same poll in different sessions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows responses from the same user for the same poll in different sessions

