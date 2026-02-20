---
id: "01KHY7PZT4NYB38JBEF9KFA2BH"
name: "banished_user_model"
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
- app/models/user_activity.rb
- spec/models/banished_user_spec.rb

## Functional Overview

This specification defines the expected behavior of `BanishedUser` within the users domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions

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
- **Model layer**: `app/models/user_activity.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to banished by.class name "User".optional
- validate uniqueness of username.case insensitive

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

