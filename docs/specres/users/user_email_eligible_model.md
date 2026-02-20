---
id: "01KHY7PZTSVX3ZTK2H1NWFSE57"
name: "user_email_eligible_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

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
- spec/models/user_email_eligible_spec.rb

## Functional Overview

This specification defines the expected behavior of `"User` within the users domain.

### Behavioral Areas

- **User email eligibility**: sets base_email_eligible to true when user meets all criteria
- **sync_base_email_eligible!**: Ensures correct behavior under the specified conditions
- **automatic synchronization callbacks**: Ensures correct behavior under the specified conditions
- **.email_eligible scope**: Ensures correct behavior under the specified conditions
- **when USE_BASE_EMAIL_ELIGIBLE_COLUMN is true**: sets base_email_eligible to true when user meets all criteria
- **when USE_BASE_EMAIL_ELIGIBLE_COLUMN is false or nil**: sets base_email_eligible to true when user meets all criteria

### Implementation Architecture

The behavior is implemented across the following layers:

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

### S-1: sets base_email_eligible to true when user meets all criteria

- **Given** the system is in a standard operational state
- **When** user meets all criteria
- **Then** sets base_email_eligible to true

### S-2: sets to false when not registered

- **Given** the system is in a standard operational state
- **When** not registered
- **Then** sets to false

### S-3: sets to false when email is blank

- **Given** the system is in a standard operational state
- **When** email is blank
- **Then** sets to false

### S-4: sets to false when suspended

- **Given** the system is in a standard operational state
- **When** suspended
- **Then** sets to false

### S-5: sets to false when spam

- **Given** the system is in a standard operational state
- **When** spam
- **Then** sets to false

### S-6: sets to false when email_newsletter is false

- **Given** the system is in a standard operational state
- **When** email_newsletter is false
- **Then** sets to false

### S-7: syncs correctly when role is removed

- **Given** the system is in a standard operational state
- **When** role is removed
- **Then** syncs correctly

### S-8: syncs when email is updated

- **Given** the system is in a standard operational state
- **When** email is updated
- **Then** syncs

### S-9: syncs when email is cleared out via update_attribute

- **Given** the system is in a standard operational state
- **When** email is cleared out via update_attribute
- **Then** syncs

### S-10: syncs when registered status changes

- **Given** the system is in a standard operational state
- **When** registered status changes
- **Then** syncs

### S-11: syncs when suspended role is added or removed

- **Given** the system is in a standard operational state
- **When** suspended role is added or removed
- **Then** syncs

### S-12: syncs when spam role is added or removed

- **Given** the system is in a standard operational state
- **When** spam role is added or removed
- **Then** syncs

