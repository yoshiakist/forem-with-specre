---
id: "01KHY7Q0FHN5NJQ1MB6JV31DFP"
name: "reaction_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/privileged_reactions_controller.rb
- app/controllers/admin/reactions_controller.rb
- app/controllers/api/v1/reactions_controller.rb
- app/controllers/reactions_controller.rb
- app/models/privileged_reaction.rb
- app/models/reaction.rb
- app/models/reaction_category.rb
- app/policies/reaction_policy.rb
- app/services/calculate_reaction_points.rb
- app/services/notifications/reactions/reaction_data.rb
- app/services/reaction_handler.rb
- app/services/slack/messengers/reaction_vomit.rb
- app/services/spam/reaction_ring_detector.rb
- app/services/users/confirm_flag_reactions.rb
- app/workers/articles/quality_reaction_worker.rb
- spec/models/reaction_spec.rb

## Functional Overview

This specification defines the expected behavior of `Reaction` within the reactions domain.

### Behavioral Areas

- **builtin validations**: Ensures correct behavior under the specified conditions
- **.user_has_been_given_too_many_spammy_article_reactions?**: Ensures correct behavior under the specified conditions
- **counter_culture**: Ensures correct behavior under the specified conditions
- **when a reaction is created**: increments reaction count on user
- **when a reaction is destroyed**: increments reaction count on user
- **validations**: Ensures correct behavior under the specified conditions
- **when user is trusted**: performs a valid query for the user
- **skip_notification_for?**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/privileged_reactions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/reactions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/reactions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/reactions_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/privileged_reaction.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/reaction.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/reaction_category.rb` -- data persistence, validations, and associations
- **Policy layer**: `app/policies/reaction_policy.rb` -- authorization and access control rules
- **Service layer**: `app/services/calculate_reaction_points.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/reactions/reaction_data.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/reaction_handler.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/slack/messengers/reaction_vomit.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to user
- validate inclusion of category.in array ReactionCategory.all slugs.map(&:to s)
- validate uniqueness of user id.scoped to %i[reactable id reactable type category]

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: performs a valid query for the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** performs a valid query for the user

### S-3: performs a valid query for the user with the include_user_profile logic

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** performs a valid query for the user with the include_user_profile logic

### S-4: increments reaction count on user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** increments reaction count on user

### S-5: decrements reaction count on user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** decrements reaction count on user

### S-6: allows like reaction for users without trusted role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows like reaction for users without trusted role

### S-7: does not allow reactions outside of allowed list

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow reactions outside of allowed list

### S-8: does not allow vomit reaction for users without trusted role

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow vomit reaction for users without trusted role

### S-9: does not allow thumbsdown reaction for users without trusted role

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow thumbsdown reaction for users without trusted role

### S-10: does not allow reaction on unpublished article

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow reaction on unpublished article

### S-11: allows vomit reactions for users with trusted role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows vomit reactions for users with trusted role

### S-12: allows thumbsdown reactions for users with trusted role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows thumbsdown reactions for users with trusted role

### S-13: is normally false

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is normally false

