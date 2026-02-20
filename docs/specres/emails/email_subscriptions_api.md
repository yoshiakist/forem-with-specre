---
id: "01KHY7Q0TBJ2W6MEYQYQX7SAEB"
name: "email_subscriptions_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/email_subscriptions_controller.rb
- spec/requests/email_subscriptions_spec.rb

## Functional Overview

This specification defines the expected behavior of `"EmailSubscriptions"` within the emails domain.

### Behavioral Areas

- **EmailSubscriptions**: Ensures correct behavior under the specified conditions
- **GET /email_subscriptions/unsubscribe**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/email_subscriptions_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns 200 if valid

- **Given** valid
- **When** the action is triggered
- **Then** returns 200

### S-2: does unsubscribe the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** does unsubscribe the user

### S-3: handles error properly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles error properly

### S-4: won

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** won

