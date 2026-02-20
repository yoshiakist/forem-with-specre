---
id: "01KHY7Q1GCGCEAMRA0Z0HE4BT3"
name: "feedback_messages_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/feedback_messages_controller.rb
- app/controllers/api/v1/feedback_messages_controller.rb
- app/controllers/feedback_messages_controller.rb
- app/helpers/feedback_messages_helper.rb
- spec/requests/feedback_messages_spec.rb

## Functional Overview

This specification defines the expected behavior of `"feedback_messages"` within the feedback domain.

### Behavioral Areas

- **feedback_messages**: Ensures correct behavior under the specified conditions
- **POST /feedback_messages**: Ensures correct behavior under the specified conditions
- **with valid params and recaptcha passed**: does not show the recaptcha tag
- **with valid params and recaptcha not configured**: does not show the recaptcha tag
- **when rate limit is reached**: sends an email when no cache
- **with valid params but recaptcha not passed**: does not show the recaptcha tag
- **when a user qualifies to bypass the recaptcha submits a report**: does not show the recaptcha tag
- **when a user doesn**: doesn

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/feedback_messages_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/feedback_messages_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/feedback_messages_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/feedback_messages_helper.rb` -- shared view utility methods


## Scenarios

### S-1: creates a feedback message

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a feedback message

### S-2: queues a slack message to be sent

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** queues a slack message to be sent

### S-3: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-4: does not show the recaptcha tag

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not show the recaptcha tag

### S-5: creates a feedback message

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a feedback message

### S-6: returns a 429

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a 429

### S-7: rerenders page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rerenders page

### S-8: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-9: creates a feedback message reported by the user without recaptcha

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a feedback message reported by the user without recaptcha

### S-10: queues a slack message to be sent

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** queues a slack message to be sent

### S-11: sends an email when no cache

- **Given** the system is in a standard operational state
- **When** no cache
- **Then** sends an email

### S-12: queues a correct email when no cache

- **Given** the system is in a standard operational state
- **When** no cache
- **Then** queues a correct email

