---
id: "01KHY7PZVA6EACCE9VAH3FYKYC"
name: "user_subscription_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/user_subscriptions_controller.rb
- app/liquid_tags/user_subscription_tag.rb
- app/models/concerns/user_subscription_sourceable.rb
- app/models/liquid_tags/user_subscription_tag.rb
- app/models/user_subscription.rb
- app/models/banished_user.rb
- app/models/concerns/algolia_searchable/searchable_user.rb
- app/models/gdpr_delete_request.rb
- app/models/identity.rb
- app/models/segmented_user.rb
- app/models/settings/authentication.rb
- app/models/settings/user_experience.rb
- app/models/user.rb
- app/models/user_activity.rb
- app/models/user_block.rb
- spec/models/user_subscription_spec.rb

## Functional Overview

This specification defines the expected behavior of `UserSubscription` within the users domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **user_subscription_sourceable**: Ensures correct behavior under the specified conditions
- **build**: Ensures correct behavior under the specified conditions
- **make**: Ensures correct behavior under the specified conditions
- **counter_culture**: Ensures correct behavior under the specified conditions
- **when a UserSubscription is created**: returns a new UserSubscription with the correct attributes
- **when a UserSubscription is destroyed**: returns a new UserSubscription with the correct attributes

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/user_subscriptions_controller.rb` -- HTTP request routing and response handling
- **Liquid tag**: `app/liquid_tags/user_subscription_tag.rb` -- custom Markdown/Liquid embed rendering
- **Model layer**: `app/models/concerns/user_subscription_sourceable.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/liquid_tags/user_subscription_tag.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/user_subscription.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/banished_user.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_user.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/gdpr_delete_request.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/identity.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/segmented_user.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/settings/authentication.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/settings/user_experience.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- validate presence of user subscription sourceable type
- validate presence of subscriber email
- validate inclusion of user subscription sourceable type.in array %w[Article]

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: validates the source is active

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates the source is active

### S-3: validates the tag is enabled in the source

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates the tag is enabled in the source

### S-4: validates the subscriber isn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates the subscriber isn

### S-5: is required on creation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is required on creation

### S-6: can be nulled on update

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** can be nulled on update

### S-7: returns a new UserSubscription with the correct attributes

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a new UserSubscription with the correct attributes

### S-8: returns a created UserSubscription with the correct attributes

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a created UserSubscription with the correct attributes

### S-9: increments subscribed_to_user_subscriptions_count on user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** increments subscribed_to_user_subscriptions_count on user

### S-10: decrements subscribed_to_user_subscriptions_count on user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** decrements subscribed_to_user_subscriptions_count on user

