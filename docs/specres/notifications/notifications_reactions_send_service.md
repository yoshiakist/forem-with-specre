---
id: "01KHY7Q074SEJSB8JD3Z52Q3G0"
name: "notifications_reactions_send_service"
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
- spec/services/notifications/reactions/send_spec.rb

## Functional Overview

This specification defines the expected behavior of `Notifications::Reactions::Send` within the notifications domain.

### Behavioral Areas

- **when data is invalid**: Ensures correct behavior under the specified conditions
- **when a reaction is ok**: Ensures correct behavior under the specified conditions
- **when a reaction is persisted and has siblings**: Ensures correct behavior under the specified conditions
- **when notification exists**: creates a notification
- **when a reaction is destroyed**: Ensures correct behavior under the specified conditions
- **when a reaction is destroyed but it has siblings**: Ensures correct behavior under the specified conditions
- **when a found reaction has unexpected json data**: creates a notification with the correct json
- **when a receiver is an organization**: Ensures correct behavior under the specified conditions

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

### S-3: creates a correct notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a correct notification

### S-4: creates a notification with the correct json

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification with the correct json

### S-5: creates a notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification

### S-6: creates a correct notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a correct notification

### S-7: creates a notification with the correct json

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification with the correct json

### S-8: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-9: returns the same notification

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the same notification

### S-10: updates the notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the notification

### S-11: updates the notification json

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the notification json

### S-12: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

