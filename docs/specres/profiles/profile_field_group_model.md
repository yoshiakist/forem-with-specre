---
id: "01KHY7Q0KBTKXKRZXDH7KNHXCS"
name: "profile_field_group_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/profile_field_groups_controller.rb
- app/controllers/profile_field_groups_controller.rb
- app/models/profile_field_group.rb
- app/models/profile.rb
- app/models/profile_field.rb
- app/models/profile_pin.rb
- spec/models/profile_field_group_spec.rb

## Functional Overview

This specification defines the expected behavior of `ProfileFieldGroup` within the profiles domain.

### Behavioral Areas

- **.onboarding**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/profile_field_groups_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/profile_field_groups_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/profile_field_group.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/profile.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/profile_field.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/profile_pin.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- have many profile fields.dependent nullify
- validate presence of name
- validate uniqueness of name

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: only returns groups that have fields for onboarding

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** only returns groups that have fields for onboarding

