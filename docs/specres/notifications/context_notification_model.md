---
id: "01KHY7Q05EDD0R985M0NPQB2R1"
name: "context_notification_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/context_notification.rb
- app/models/notification.rb
- app/models/notification_subscription.rb
- app/models/users/notification_setting.rb
- app/models/welcome_notification.rb
- spec/models/context_notification_spec.rb

## Functional Overview

This specification defines the expected behavior of `ContextNotification` within the notifications domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/context_notification.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/notification.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/notification_subscription.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/users/notification_setting.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/welcome_notification.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- be valid
- belong to context
- validate presence of action
- validate presence of context type
- validate uniqueness of context id.scoped to %i[context type action]

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: is invalid with a Comment as context

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is invalid with a Comment as context

