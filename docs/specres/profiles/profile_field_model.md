---
id: "01KHY7Q0KEGDXX397FH2M5C724"
name: "profile_field_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/profile_field_groups_controller.rb
- app/controllers/admin/profile_fields_controller.rb
- app/controllers/profile_field_groups_controller.rb
- app/models/profile_field.rb
- app/models/profile_field_group.rb
- app/models/profile.rb
- app/models/profile_pin.rb
- spec/models/profile_field_spec.rb

## Functional Overview

This specification defines the expected behavior of `ProfileField` within the profiles domain.

### Behavioral Areas

- **associations**: Ensures correct behavior under the specified conditions
- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions
- **maximum_header_field_count**: Ensures correct behavior under the specified conditions
- **callbacks**: Ensures correct behavior under the specified conditions
- **maximum_header_field_count**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/profile_field_groups_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/profile_fields_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/profile_field_groups_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/profile_field.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/profile_field_group.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/profile.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/profile_pin.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to profile field group
- validate presence of attribute name.on update
- validate presence of display area
- validate presence of input type
- validate presence of label

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: ensures the label is case-insensitively unique

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** ensures the label is case-insensitively unique

### S-3: limits the number of header fields on create

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** limits the number of header fields on create

### S-4: limits the number of header fields on update

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** limits the number of header fields on update

### S-5: considers existing header fields valid even if we reached the maximum

- **Given** we reached the maximum
- **When** the action is triggered
- **Then** considers existing header fields valid even

### S-6: automatically generates an attribute name

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** automatically generates an attribute name

### S-7: limits the number of header fields

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** limits the number of header fields

