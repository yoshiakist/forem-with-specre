---
id: "01KHY7PZTP21KAZGT354R5VXG1"
name: "user_block_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/user_blocks_controller.rb
- app/models/user_block.rb
- app/policies/user_block_policy.rb
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
- spec/models/user_block_spec.rb

## Functional Overview

This specification defines the expected behavior of `UserBlock` within the users domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/user_blocks_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/user_block.rb` -- data persistence, validations, and associations
- **Policy layer**: `app/policies/user_block_policy.rb` -- authorization and access control rules
- **Model layer**: `app/models/banished_user.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_user.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/user_subscription_sourceable.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/gdpr_delete_request.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/identity.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/liquid_tags/user_subscription_tag.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/segmented_user.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/settings/authentication.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/settings/user_experience.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- validate inclusion of config.in array %w[default]

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: prevents the blocker from blocking itself

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** prevents the blocker from blocking itself

### S-3: returns ids blocked by user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns ids blocked by user

### S-4: busts user block cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts user block cache

