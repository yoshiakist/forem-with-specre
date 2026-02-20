---
id: "01KHY7Q0SY0YTD4E0316G9PKX0"
name: "email_authorization_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/email_authorizations_controller.rb
- app/models/email_authorization.rb
- app/models/blocked_email_domain.rb
- app/models/email.rb
- app/models/email_message.rb
- spec/models/email_authorization_spec.rb

## Functional Overview

This specification defines the expected behavior of `EmailAuthorization` within the emails domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions
- **confirmation_token**: Ensures correct behavior under the specified conditions
- **sent_at**: Ensures correct behavior under the specified conditions
- **.last_verification_date**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/email_authorizations_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/email_authorization.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/blocked_email_domain.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/email.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/email_message.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- validate inclusion of type of.in array EmailAuthorization::TYPES
- validate presence of type of

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: is created automatically

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is created automatically

### S-3: is not changed if already present

- **Given** already present
- **When** the action is triggered
- **Then** is not changed

### S-4: is aliased to #created_at

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is aliased to #created_at

### S-5: returns nil if there are no email authorizations

- **Given** there are no email authorizations
- **When** the action is triggered
- **Then** returns nil

### S-6: does not return unverified email authorizations

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not return unverified email authorizations

### S-7: returns the last email authorization

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the last email authorization

