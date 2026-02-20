---
id: "01KHY7Q06TTYF8WT5VP81RFA2P"
name: "notifications_new_follower_send_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/notifications/milestone/send.rb
- app/services/notifications/moderation/send.rb
- app/services/notifications/new_badge_achievement/send.rb
- app/services/notifications/new_comment/send.rb
- app/services/notifications/new_follower/send.rb
- app/services/notifications/new_mention/send.rb
- app/services/notifications/notifiable_action/send.rb
- app/services/notifications/reactions/send.rb
- app/services/notifications/subforem_change_notification/send.rb
- app/services/notifications/tag_adjustment_notification/send.rb
- app/services/notifications/welcome_notification/send.rb
- app/services/push_notifications/send.rb
- app/workers/badge_achievements/send_email_notification_worker.rb
- app/workers/broadcasts/send_welcome_notifications_worker.rb
- app/workers/comments/send_email_notification_worker.rb
- spec/services/notifications/new_follower/send_spec.rb

## Functional Overview

This specification defines the expected behavior of `Notifications::NewFollower::Send` within the notifications domain.

### Behavioral Areas

- **when trying to pass tag follow data**: creates a notification with data
- **when trying to pass follow data as a Hash with keys as strings**: creates a notification with data
- **when user follows another user**: creates a notification with user data
- **when destroyed follow**: Ensures correct behavior under the specified conditions
- **when 2 user follows another user**: creates a notification with user data
- **when notification exists**: creates a notification
- **when destroyed follow and notification exists**: creates a notification

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/notifications/milestone/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/moderation/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/new_badge_achievement/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/new_comment/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/new_follower/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/new_mention/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/notifiable_action/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/reactions/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/subforem_change_notification/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/tag_adjustment_notification/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/welcome_notification/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/push_notifications/send.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: raises an exception

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises an exception

### S-2: creates a notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification

### S-3: creates a notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification

### S-4: creates a notification with data

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification with data

### S-5: creates a read notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a read notification

### S-6: does not create a notification

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create a notification

### S-7: destroys notification if it exists

- **Given** it exists
- **When** the action is triggered
- **Then** destroys notification

### S-8: destroys the correct notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** destroys the correct notification

### S-9: creates a notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification

### S-10: creates a notification with data

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification with data

### S-11: creates a notification with user data

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification with user data

### S-12: does not include suspended users in aggregated_siblings

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not include suspended users in aggregated_siblings

