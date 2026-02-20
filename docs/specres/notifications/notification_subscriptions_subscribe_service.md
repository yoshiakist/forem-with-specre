---
id: "01KHY7Q068FK8WWF1W99PP3MTK"
name: "notification_subscriptions_subscribe_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/notification_subscriptions/subscribe.rb
- app/services/notification_subscriptions/unsubscribe.rb
- app/controllers/notification_subscriptions_controller.rb
- app/services/notification_subscriptions/update.rb
- app/workers/notification_subscriptions/update_worker.rb
- spec/services/notification_subscriptions/subscribe_spec.rb

## Functional Overview

This specification defines the expected behavior of `NotificationSubscriptions::Subscribe` within the notifications domain.

### Behavioral Areas

- **when subscribing to a comment**: creates a notification subscription for the comment
- **when subscribing to an article**: creates a notification subscription for the article
- **when subscribing to a top-level comment**: creates a notification subscription for the comment
- **when already subscribed**: Ensures correct behavior under the specified conditions
- **when parameters are missing**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/notification_subscriptions/subscribe.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notification_subscriptions/unsubscribe.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/notification_subscriptions_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/notification_subscriptions/update.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/notification_subscriptions/update_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: creates a notification subscription for the comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification subscription for the comment

### S-2: creates a notification subscription for the article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification subscription for the article

### S-3: can override subscription config (if valid)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** can override subscription config (if valid)

### S-4: cannot override subscription config (if invalid)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** cannot override subscription config (if invalid)

### S-5: creates a notification subscription for the top-level comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification subscription for the top-level comment

### S-6: returns the existing subscription without creating anything new

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the existing subscription without creating anything new

### S-7: does not create a notification subscription

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create a notification subscription

