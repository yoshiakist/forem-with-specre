---
id: "01KHY7Q08TJRA0X568774PNAMZ"
name: "notifications_notifiable_action_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/notifications/notifiable_action_worker.rb
- app/controllers/notifications/counts_controller.rb
- app/controllers/notifications/reads_controller.rb
- app/controllers/notifications_controller.rb
- app/helpers/notifications_helper.rb
- app/services/notifications.rb
- app/services/notifications/milestone/send.rb
- app/services/notifications/moderation/send.rb
- app/services/notifications/new_badge_achievement/send.rb
- app/services/notifications/new_comment/send.rb
- app/services/notifications/new_follower/follow_data.rb
- spec/workers/notifications/notifiable_action_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Notifications::NotifiableActionWorker` within the notifications domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/notifications/notifiable_action_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/notifications/counts_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/notifications/reads_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/notifications_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/notifications_helper.rb` -- shared view utility methods
- **Service layer**: `app/services/notifications.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/milestone/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/moderation/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/new_badge_achievement/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/new_comment/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/new_follower/follow_data.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: calls the service when existing notifiable passed

- **Given** the system is in a standard operational state
- **When** existing notifiable passed
- **Then** calls the service

### S-2: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-3: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

