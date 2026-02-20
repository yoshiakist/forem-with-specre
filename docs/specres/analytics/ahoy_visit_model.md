---
id: "01KHY7Q0YSRQWQWD62KP3Z1KN3"
name: "ahoy_visit_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/ahoy/visit.rb
- app/controllers/ahoy/email_clicks_controller.rb
- app/models/ahoy/event.rb
- spec/models/ahoy/visit_spec.rb

## Functional Overview

This specification defines the expected behavior of `Ahoy::Visit` within the analytics domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions
- **fast_destroy_old_notifications**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/ahoy/visit.rb` -- data persistence, validations, and associations
- **Controller layer**: `app/controllers/ahoy/email_clicks_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/ahoy/event.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- have many events.class name "Ahoy::Event".dependent destroy
- belong to user.optional

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: bulk deletes visits older than given timestamp

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** bulk deletes visits older than given timestamp

