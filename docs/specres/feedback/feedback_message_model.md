---
id: "01KHY7Q1G748J6SQ4ZJ8CDRMTT"
name: "feedback_message_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/feedback_messages_controller.rb
- app/controllers/api/v1/feedback_messages_controller.rb
- app/controllers/feedback_messages_controller.rb
- app/helpers/feedback_messages_helper.rb
- app/models/feedback_message.rb
- spec/models/feedback_message_spec.rb

## Functional Overview

This specification defines the expected behavior of `FeedbackMessage` within the feedback domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions
- **validations for an abuse report**: does not check for uniqueness if the new abuse report does not have a reporter id
- **validations for a bug report**: does not check for uniqueness if the new abuse report does not have a reporter id
- **.all_user_reports**: Ensures correct behavior under the specified conditions
- **determine_reported_from_url**: Ensures correct behavior under the specified conditions
- **when the URL matches a Billboard**: sets the reported object to the corresponding Billboard
- **when the URL matches an Article**: sets the reported object to the corresponding Article

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/feedback_messages_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/feedback_messages_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/feedback_messages_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/feedback_messages_helper.rb` -- shared view utility methods
- **Model layer**: `app/models/feedback_message.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to offender.class name "User".inverse of offender feedback messages.optional
- belong to reporter.class name "User".inverse of reporter feedback messages.optional
- belong to affected.class name "User".inverse of affected feedback messages.optional
- have one email message.dependent nullify.optional
- have many notes.inverse of noteable.dependent destroy
- validate presence of feedback type
- validate presence of message
- validate length of reported url.is at most 250
- validate length of message.is at most 2500
- validate presence of reported url
- validate length of reported url.is at most 250
- validate presence of category

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: does not check for uniqueness if the new abuse report does not have a reporter i...

- **Given** the new abuse report does not have a reporter id
- **When** the action is triggered
- **Then** does not check for uniqueness

### S-3: returns reported feedback messages

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns reported feedback messages

### S-4: returns affected feedback messages

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns affected feedback messages

### S-5: returns offender feedback messages

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns offender feedback messages

### S-6: sets the reported object to the corresponding Billboard

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the reported object to the corresponding Billboard

### S-7: sets the reported object to the corresponding Article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the reported object to the corresponding Article

### S-8: sets the reported object to the corresponding Comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the reported object to the corresponding Comment

### S-9: sets the reported object to the corresponding User

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the reported object to the corresponding User

### S-10: does not set the reported object

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not set the reported object

