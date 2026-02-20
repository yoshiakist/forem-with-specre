---
id: "01KHY7PZT7NW2BX66EHC1SRDHE"
name: "identity_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/identity.rb
- app/workers/users/bust_profile_identity_cache_worker.rb
- app/models/banished_user.rb
- app/models/concerns/algolia_searchable/searchable_user.rb
- app/models/concerns/user_subscription_sourceable.rb
- app/models/gdpr_delete_request.rb
- app/models/liquid_tags/user_subscription_tag.rb
- app/models/segmented_user.rb
- app/models/settings/authentication.rb
- app/models/settings/user_experience.rb
- app/models/user.rb
- app/models/user_activity.rb
- spec/models/identity_spec.rb

## Functional Overview

This specification defines the expected behavior of `Identity` within the users domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions
- **.build_build_from_omniauth**: Ensures correct behavior under the specified conditions
- **with Apple payload**: initializes a new identity from the auth payload
- **with Github payload**: initializes a new identity from the auth payload
- **with Facebook payload**: initializes a new identity from the auth payload
- **with Forem payload**: initializes a new identity from the auth payload
- **with Twitter payload**: initializes a new identity from the auth payload

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/identity.rb` -- data persistence, validations, and associations
- **Background worker**: `app/workers/users/bust_profile_identity_cache_worker.rb` -- asynchronous job processing
- **Model layer**: `app/models/banished_user.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_user.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/user_subscription_sourceable.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/gdpr_delete_request.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/liquid_tags/user_subscription_tag.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/segmented_user.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/settings/authentication.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/settings/user_experience.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/user.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/user_activity.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to user
- validate presence of provider
- validate presence of uid
- validate uniqueness of uid.scoped to provider
- validate uniqueness of user id.scoped to provider
- validate inclusion of provider.in array Authentication::Providers.available.map(&:to s)
- serialize auth data dump

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: initializes a new identity from the auth payload

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** initializes a new identity from the auth payload

### S-3: finds an existing identity

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** finds an existing identity

### S-4: initializes a new identity from the auth payload

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** initializes a new identity from the auth payload

### S-5: finds an existing identity

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** finds an existing identity

### S-6: initializes a new identity from the auth payload

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** initializes a new identity from the auth payload

### S-7: finds an existing identity

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** finds an existing identity

### S-8: initializes a new identity from the auth payload

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** initializes a new identity from the auth payload

### S-9: finds an existing identity

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** finds an existing identity

### S-10: initializes a new identity from the auth payload

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** initializes a new identity from the auth payload

### S-11: finds an existing identity

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** finds an existing identity

### S-12: does not store the access token in auth_data_dump

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not store the access token in auth_data_dump

### S-13: returns the email associated with the identity

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the email associated with the identity

