---
id: "01KHY7Q0TNCNQ2D6YAK5TCAZXR"
name: "email_subscriptions_unsubscribe.html.erb_view"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/email_subscriptions_controller.rb
- spec/views/email_subscriptions/unsubscribe.html.erb_spec.rb

## Functional Overview

This specification defines the expected behavior of `"email_subscriptions/unsubscribe"` within the emails domain.

### Behavioral Areas

- **email_subscriptions/unsubscribe**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/email_subscriptions_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: has unsubscribed info

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** has unsubscribed info

