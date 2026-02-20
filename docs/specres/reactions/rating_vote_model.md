---
id: "01KHY7Q0F93NZ82JZC341GD32T"
name: "rating_vote_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/rating_votes_controller.rb
- app/models/rating_vote.rb
- app/policies/rating_vote_policy.rb
- app/models/poll_option.rb
- app/models/poll_skip.rb
- app/models/poll_text_response.rb
- app/models/poll_vote.rb
- app/models/privileged_reaction.rb
- app/models/reaction.rb
- app/models/reaction_category.rb
- spec/models/rating_vote_spec.rb

## Functional Overview

This specification defines the expected behavior of `RatingVote` within the reactions domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions
- **uniqueness**: Ensures correct behavior under the specified conditions
- **modifies article rating score**: does allow a user to create one rating for one article
- **permissions**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/rating_votes_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/rating_vote.rb` -- data persistence, validations, and associations
- **Policy layer**: `app/policies/rating_vote_policy.rb` -- authorization and access control rules
- **Model layer**: `app/models/poll_option.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_skip.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_text_response.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_vote.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/privileged_reaction.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/reaction.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/reaction_category.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to article
- belong to user.optional
- validate inclusion of context.in array %w[explicit readinglist reaction comment]
- validate inclusion of group.in array %w[experience level]
- validate numericality of rating.is greater than 0.0.is less than or equal to 10.0
- validate uniqueness of user id.scoped to %i[article id context]

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: does allow a user to create one rating for one article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** does allow a user to create one rating for one article

### S-3: does not allow a user to create multiple ratings for one article

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow a user to create multiple ratings for one article

### S-4: does allows more than one reaction if different contexts

- **Given** different contexts
- **When** the action is triggered
- **Then** does allows more than one reaction

### S-5: does allows more than one two reactions if all different contexts

- **Given** all different contexts
- **When** the action is triggered
- **Then** does allows more than one two reactions

### S-6: assigns article rating

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** assigns article rating

### S-7: allows untrusted user to leave readinglist_reaction context rating

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows untrusted user to leave readinglist_reaction context rating

### S-8: allows trusted users to make explicit rating

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows trusted users to make explicit rating

### S-9: does not allow non-trusted users to make rating

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow non-trusted users to make rating

### S-10: does allows author to make rating on own post

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** does allows author to make rating on own post

