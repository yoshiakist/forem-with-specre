---
id: "01KHY7Q06DB08AG515JS0VHH9H"
name: "notification_subscriptions_update_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/notification_subscriptions/update.rb
- app/services/notifications/update.rb
- app/workers/notification_subscriptions/update_worker.rb
- app/workers/notifications/update_worker.rb
- app/controllers/notification_subscriptions_controller.rb
- app/services/notification_subscriptions/subscribe.rb
- app/services/notification_subscriptions/unsubscribe.rb
- spec/services/notification_subscriptions/update_spec.rb

## Functional Overview

This specification defines the expected behavior of `NotificationSubscriptions::Update` within the notifications domain.

### Behavioral Areas

- **when updating notification subscriptions of an article**: updates all notification subscriptions for the article

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/notification_subscriptions/update.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/update.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/notification_subscriptions/update_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/notifications/update_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/notification_subscriptions_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/notification_subscriptions/subscribe.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notification_subscriptions/unsubscribe.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: updates all notification subscriptions for the article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates all notification subscriptions for the article

