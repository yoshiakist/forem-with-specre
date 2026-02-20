---
id: "01KHY7Q06N8TKYXRNF5TWQWCEY"
name: "notifications_new_badge_achievement_send_service"
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
- spec/services/notifications/new_badge_achievement/send_spec.rb

## Functional Overview

This specification defines the expected behavior of `Notifications::NewBadgeAchievement::Send` within the notifications domain.

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

### S-1: creates a notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification

### S-2: creates a notification for the badge achievement user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification for the badge achievement user

### S-3: creates a notification for the badge achievement

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification for the badge achievement

### S-4: creates a notification with no action

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification with no action

### S-5: creates a notification with the proper json data

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification with the proper json data

