---
id: "01KHY7Q06JGKGN4DAAYAEW58MX"
name: "notifications_moderation_send_service"
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
- spec/services/notifications/moderation/send_spec.rb

## Functional Overview

This specification defines the expected behavior of `Notifications::Moderation::Send` within the notifications domain.

### Behavioral Areas

- **when notifying on comments**: Ensures correct behavior under the specified conditions
- **when the comment**: calls comment_data since parameter is a comment
- **when notifying on articles**: Ensures correct behavior under the specified conditions
- **when the article**: calls article_data since parameter is an article

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

### S-1: calls comment_data since parameter is a comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls comment_data since parameter is a comment

### S-2: checks whether Notification is inserted on DB

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** checks whether Notification is inserted on DB

### S-3: checks whether created Notification is valid

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** checks whether created Notification is valid

### S-4: checks that moderator last notification time updates

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** checks that moderator last notification time updates

### S-5: does not create a notification if the moderator is the comment

- **Given** the moderator is the comment
- **When** the action is triggered
- **Then** does not create a notification

### S-6: includes all needed user data in the notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes all needed user data in the notification

### S-7: does not create a notification

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create a notification

### S-8: calls article_data since parameter is an article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls article_data since parameter is an article

### S-9: checks whether Notification is inserted on DB

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** checks whether Notification is inserted on DB

### S-10: checks whether created Notification is valid

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** checks whether created Notification is valid

### S-11: checks that moderator last notification time updates

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** checks that moderator last notification time updates

### S-12: does not create a notification if the moderator is the article

- **Given** the moderator is the article
- **When** the action is triggered
- **Then** does not create a notification

