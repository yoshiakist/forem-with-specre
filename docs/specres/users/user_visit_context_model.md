---
id: "01KHY7PZVDV7G270NCRA8FS30W"
name: "user_visit_context_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/user_visit_context.rb
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
- spec/models/user_visit_context_spec.rb

## Functional Overview

This specification defines the expected behavior of `UserVisitContext` within the users domain.

### Behavioral Areas

- **associations**: Ensures correct behavior under the specified conditions
- **callbacks**: Ensures correct behavior under the specified conditions
- **set_user_language**: calls set_user_language after create

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/user_visit_context.rb` -- data persistence, validations, and associations
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
- have many ahoy visits.class name "Ahoy::Visit".dependent nullify

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: calls set_user_language after create

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls set_user_language after create

### S-3: creates UserLanguage records

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates UserLanguage records

### S-4: logs an error if something goes wrong

- **Given** something goes wrong
- **When** the action is triggered
- **Then** logs an error

### S-5: matches specific languages

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** matches specific languages

