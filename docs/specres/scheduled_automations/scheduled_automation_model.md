---
id: "01KHY7Q1JDHPATCGZHEBBFCTMQ"
name: "scheduled_automation_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/scheduled_automations_controller.rb
- app/helpers/scheduled_automations_helper.rb
- app/models/scheduled_automation.rb
- spec/models/scheduled_automation_spec.rb

## Functional Overview

This specification defines the expected behavior of `ScheduledAutomation` within the scheduled_automations domain.

### Behavioral Areas

- **associations**: Ensures correct behavior under the specified conditions
- **validations**: Ensures correct behavior under the specified conditions
- **when user is not a community bot or admin**: Ensures correct behavior under the specified conditions
- **when user is an admin**: Ensures correct behavior under the specified conditions
- **when user is a community bot**: Ensures correct behavior under the specified conditions
- **frequency_config normalization**: Ensures correct behavior under the specified conditions
- **frequency_config validations**: Ensures correct behavior under the specified conditions
- **with hourly frequency**: is valid with correct minute

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/scheduled_automations_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/scheduled_automations_helper.rb` -- shared view utility methods
- **Model layer**: `app/models/scheduled_automation.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to user
- validate presence of frequency
- validate presence of action
- validate presence of service name
- validate presence of state
- validate inclusion of frequency.in array %w[daily weekly hourly custom interval]
- validate inclusion of action.in array %w[create draft publish article award first org post badge]
- validate inclusion of state.in array %w[active running completed failed]

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: is invalid

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is invalid

### S-3: is valid

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is valid

### S-4: is valid

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is valid

### S-5: converts string values to integers before validation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** converts string values to integers before validation

### S-6: keeps integer values as integers

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** keeps integer values as integers

### S-7: preserves non-numeric string values

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** preserves non-numeric string values

### S-8: handles mixed integer and string values

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles mixed integer and string values

### S-9: is valid with correct minute

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is valid with correct minute

### S-10: is invalid without minute

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is invalid without minute

### S-11: is invalid with minute out of range

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is invalid with minute out of range

### S-12: is valid with correct hour and minute

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is valid with correct hour and minute

### S-13: is invalid without hour

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is invalid without hour

