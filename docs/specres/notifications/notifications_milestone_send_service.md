---
id: "01KHY7Q06FX75GD03FH2GSA2RZ"
name: "notifications_milestone_send_service"
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
- spec/services/notifications/milestone/send_spec.rb

## Functional Overview

This specification defines the expected behavior of `Notifications::Milestone::Send` within the notifications domain.

### Behavioral Areas

- **when a user has never received a milestone notification**: sends the appropriate level view milestone notification
- **when a user has received a milestone notification before**: sends the appropriate level view milestone notification
- **When send view type milestone notification**: sends the appropriate level view milestone notification
- **when an article is related to an organization**: creates another notification related to organization

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

### S-1: sends the appropriate level view milestone notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends the appropriate level view milestone notification

### S-2: sends the appropriate level reaction milestone notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends the appropriate level reaction milestone notification

### S-3: sends the appropriate level view milestone notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends the appropriate level view milestone notification

### S-4: adds an additional view milestone notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds an additional view milestone notification

### S-5: does not the same view milestone notification if called again

- **Given** called again
- **When** the action is triggered
- **Then** does not the same view milestone notification

### S-6: does not send a view milestone notification again if the latest num of views isn

- **Given** the latest num of views isn
- **When** the action is triggered
- **Then** does not send a view milestone notification again

### S-7: checks notification json data

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** checks notification json data

### S-8: sends the appropriate level reaction milestone notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends the appropriate level reaction milestone notification

### S-9: creates another notification related to organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates another notification related to organization

