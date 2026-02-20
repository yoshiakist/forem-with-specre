---
id: "01KHY7Q0T1A7TGDGR3W46D385Z"
name: "email_message_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/email_messages_controller.rb
- app/models/email_message.rb
- app/models/blocked_email_domain.rb
- app/models/email.rb
- app/models/email_authorization.rb
- spec/models/email_message_spec.rb

## Functional Overview

This specification defines the expected behavior of `EmailMessage` within the emails domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **fast_destroy_old_notifications**: Ensures correct behavior under the specified conditions
- **Handles html and non html content**: return correct content with no html

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/email_messages_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/email_message.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/blocked_email_domain.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/email.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/email_authorization.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to feedback message.optional

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: bulk deletes emails older than given timestamp

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** bulk deletes emails older than given timestamp

### S-3: return correct content with no html

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** return correct content with no html

### S-4: return correct content with html

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** return correct content with html

### S-5: return correct content with nil

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** return correct content with nil

