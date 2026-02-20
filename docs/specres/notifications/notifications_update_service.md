---
id: "01KHY7Q07EKHWX56E9HPFQS423"
name: "notifications_update_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/notification_subscriptions/update.rb
- app/services/notifications/update.rb
- app/workers/notification_subscriptions/update_worker.rb
- app/workers/notifications/update_worker.rb
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
- spec/services/notifications/update_spec.rb

## Functional Overview

This specification defines the expected behavior of `Notifications::Update` within the notifications domain.

### Behavioral Areas

- **when updating notifications of an article**: updates all notifications with the same action
- **when updating notifications of an organization article**: updates all notifications with the same action
- **when updating notifications on a comment**: updates all notifications with the same action
- **when updating notifications on a reaction**: updates all notifications with the same action

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/notification_subscriptions/update.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/update.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/notification_subscriptions/update_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/notifications/update_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/notifications/counts_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/notifications/reads_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/notifications_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/notifications_helper.rb` -- shared view utility methods
- **Service layer**: `app/services/notifications.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/milestone/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/moderation/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/new_badge_achievement/send.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: updates all notifications with the same action

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates all notifications with the same action

### S-2: does not update notifications with a different action

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not update notifications with a different action

### S-3: updates all notifications with the same action

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates all notifications with the same action

### S-4: does not update notifications with a different action

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not update notifications with a different action

### S-5: updates all notifications

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates all notifications

### S-6: does not update notifications

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not update notifications

