---
id: "01KHY7Q08A1606Q0ER5RER1SEE"
name: "notifications_create_round_robin_moderation_notifications_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/notifications/create_round_robin_moderation_notifications_worker.rb
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
- spec/workers/notifications/create_round_robin_moderation_notifications_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Notifications::CreateRoundRobinModerationNotificationsWorker` within the notifications domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **When available moderator(s) + comment**: Ensures correct behavior under the specified conditions
- **when available moderator(s) + article**: Ensures correct behavior under the specified conditions
- **when no available moderator for comment**: Ensures correct behavior under the specified conditions
- **when no available moderator for article**: Ensures correct behavior under the specified conditions
- **when no valid comment or article**: Ensures correct behavior under the specified conditions
- **when no valid comment/article + no moderator**: Ensures correct behavior under the specified conditions
- **when the notifiable user is limited**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/notifications/create_round_robin_moderation_notifications_worker.rb` -- asynchronous job processing
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

### S-1: calls the service

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls the service

### S-2: calls the service

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls the service

### S-3: does not call the service

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call the service

### S-4: does not call the service

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call the service

### S-5: does not call the service

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call the service

### S-6: does not call the service

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call the service

### S-7: does not call the send service

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call the send service

### S-8: does not call the service

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call the service

### S-9: does not call the service

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call the service

### S-10: does not call the service

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call the service

