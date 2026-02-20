---
id: "01KHY7Q06ZDR45CW1KFMZTTF7P"
name: "notifications_notifiable_action_send_service"
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
- spec/services/notifications/notifiable_action/send_spec.rb

## Functional Overview

This specification defines the expected behavior of `Notifications::NotifiableAction::Send` within the notifications domain.

### Behavioral Areas

- **when following a user or organization**: creates a correct user notification
- **when following a user or organization and being mentioned in an article**: creates a correct user notification
- **when publishing an article under an organization**: creates a correct organization notification

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

### S-1: creates notifications

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates notifications

### S-2: creates a correct user notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a correct user notification

### S-3: creates a correct organization notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a correct organization notification

### S-4: creates a context notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a context notification

### S-5: creates a correct context notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a correct context notification

### S-6: does not create a notification if the follower has muted the user

- **Given** the follower has muted the user
- **When** the action is triggered
- **Then** does not create a notification

### S-7: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-8: upserts the existing notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** upserts the existing notification

### S-9: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-10: does not create a notification when following a user

- **Given** the system is in a standard operational state
- **When** following a user
- **Then** does not create a notification

### S-11: does not create a notification when following an organization

- **Given** the system is in a standard operational state
- **When** following an organization
- **Then** does not create a notification

### S-12: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

