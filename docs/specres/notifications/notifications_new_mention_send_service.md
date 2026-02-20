---
id: "01KHY7Q06WRCDETKM2Z5SHFGTJ"
name: "notifications_new_mention_send_service"
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
- spec/services/notifications/new_mention/send_spec.rb

## Functional Overview

This specification defines the expected behavior of `Notifications::NewMention::Send` within the notifications domain.

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

### S-1: creates a mention notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a mention notification

### S-2: creates a correct mention notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a correct mention notification

### S-3: sends from proper mentioner

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends from proper mentioner

### S-4: creates users notifications

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates users notifications

### S-5: creates a correct user notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a correct user notification

### S-6: creates a mobile notification with name of the mentionable author

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a mobile notification with name of the mentionable author

### S-7: does not send if the article has negative score already

- **Given** the article has negative score already
- **When** the action is triggered
- **Then** does not send

### S-8: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

