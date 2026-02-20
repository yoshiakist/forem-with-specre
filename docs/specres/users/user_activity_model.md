---
id: "01KHY7PZTM64XJXZ0YX9XHA9QP"
name: "user_activity_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/user_activity.rb
- app/models/banished_user.rb
- app/models/concerns/algolia_searchable/searchable_user.rb
- app/models/concerns/user_subscription_sourceable.rb
- app/models/gdpr_delete_request.rb
- app/models/identity.rb
- app/models/liquid_tags/user_subscription_tag.rb
- app/models/segmented_user.rb
- app/models/settings/authentication.rb
- app/models/settings/user_experience.rb
- app/models/user.rb
- spec/models/user_activity_spec.rb

## Functional Overview

This specification defines the expected behavior of `UserActivity` within the users domain.

### Behavioral Areas

- **set_activity!**: Ensures correct behavior under the specified conditions
- **when there are page views with a mix of tracked times**: stores exactly the 20 most recent page-views in descending order
- **when a UserActivity already exists for the user**: populates alltime_tags from the user
- **associations**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/user_activity.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/banished_user.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_user.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/user_subscription_sourceable.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/gdpr_delete_request.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/identity.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/liquid_tags/user_subscription_tag.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/segmented_user.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/settings/authentication.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/settings/user_experience.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/user.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to user

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: sets last_activity_at to now

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets last_activity_at to now

### S-3: stores exactly the 20 most recent page-views in descending order

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** stores exactly the 20 most recent page-views in descending order

### S-4: includes only views with time_tracked_in_seconds > 29 in recent_* aggregations

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes only views with time_tracked_in_seconds > 29 in recent_* aggregations

### S-5: captures recent_subforems from those same articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** captures recent_subforems from those same articles

### S-6: populates alltime_tags from the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** populates alltime_tags from the user

### S-7: populates alltime_users from the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** populates alltime_users from the user

### S-8: populates alltime_organizations from the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** populates alltime_organizations from the user

### S-9: populates alltime_subforems from the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** populates alltime_subforems from the user

### S-10: combines recent_tags and alltime_tags in #relevant_tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** combines recent_tags and alltime_tags in #relevant_tags

### S-11: updates the same record instead of creating a new one

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the same record instead of creating a new one

