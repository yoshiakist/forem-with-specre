---
id: "01KHY7Q0883KGGTSCA8V7YVMFH"
name: "notification_subscriptions_update_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/notification_subscriptions/update_worker.rb
- app/workers/notifications/update_worker.rb
- app/controllers/notification_subscriptions_controller.rb
- app/services/notification_subscriptions/subscribe.rb
- app/services/notification_subscriptions/unsubscribe.rb
- app/services/notification_subscriptions/update.rb
- spec/workers/notification_subscriptions/update_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `NotificationSubscriptions::UpdateWorker` within the notifications domain.

### Behavioral Areas

- **perform_now**: Ensures correct behavior under the specified conditions
- **when wrong class is passed**: Ensures correct behavior under the specified conditions
- **when notifiable is not found**: Ensures correct behavior under the specified conditions
- **when notifiable is found**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/notification_subscriptions/update_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/notifications/update_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/notification_subscriptions_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/notification_subscriptions/subscribe.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notification_subscriptions/unsubscribe.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notification_subscriptions/update.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: raises an exception

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises an exception

### S-2: does not call the service

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call the service

### S-3: calls the service

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls the service

