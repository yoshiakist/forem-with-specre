---
id: "01KHY7Q06AED3WMEP28671MT6E"
name: "notification_subscriptions_unsubscribe_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/notification_subscriptions/unsubscribe.rb
- app/controllers/notification_subscriptions_controller.rb
- app/services/notification_subscriptions/subscribe.rb
- app/services/notification_subscriptions/update.rb
- app/workers/notification_subscriptions/update_worker.rb
- spec/services/notification_subscriptions/unsubscribe_spec.rb

## Functional Overview

This specification defines the expected behavior of `NotificationSubscriptions::Unsubscribe` within the notifications domain.

### Behavioral Areas

- **when a valid subscription ID is provided**: destroys the notification subscription
- **when an invalid subscription ID is provided**: destroys the notification subscription
- **when no subscription ID is provided**: destroys the notification subscription

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/notification_subscriptions/unsubscribe.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/notification_subscriptions_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/notification_subscriptions/subscribe.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notification_subscriptions/update.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/notification_subscriptions/update_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: destroys the notification subscription

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** destroys the notification subscription

### S-2: does not destroy any notification subscriptions

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not destroy any notification subscriptions

### S-3: does not destroy any notification subscriptions

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not destroy any notification subscriptions

