---
id: "01KHY7Q05H5EX8BY9VF9QBX5Q5"
name: "notification_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/notification_subscriptions_controller.rb
- app/controllers/notifications_controller.rb
- app/controllers/users/notification_settings_controller.rb
- app/decorators/notification_decorator.rb
- app/helpers/notifications_helper.rb
- app/mailers/organization_membership_notification_mailer.rb
- app/models/context_notification.rb
- app/models/notification.rb
- app/models/notification_subscription.rb
- app/models/users/notification_setting.rb
- app/models/welcome_notification.rb
- app/services/audit/notification.rb
- app/services/notifications.rb
- app/workers/badge_achievements/send_email_notification_worker.rb
- app/workers/broadcasts/send_welcome_notifications_worker.rb
- spec/models/notification_spec.rb

## Functional Overview

This specification defines the expected behavior of `Notification` within the notifications domain.

### Behavioral Areas

- **when trying to create duplicate notifications**: creates a notification belonging to the person being followed
- **when notifiable is an Article**: sends a notification to the author of the article
- **when notifiable is a Comment**: does not send a notification to the author of the article if the commenter is the author
- **when callbacks are triggered after create**: creates a notification belonging to the person being followed
- **send_new_follower_notification**: Ensures correct behavior under the specified conditions
- **when trying to a send notification after following a tag**: does not enqueue a notification job
- **when trying to send a notification after following a user**: validates a unique user_id according to the correct scope
- **when a user follows an organization**: validates a unique user_id according to the correct scope

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/notification_subscriptions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/notifications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/notification_settings_controller.rb` -- HTTP request routing and response handling
- **Decorator**: `app/decorators/notification_decorator.rb` -- presentation logic and view-model enrichment
- **View helper**: `app/helpers/notifications_helper.rb` -- shared view utility methods
- **Mailer**: `app/mailers/organization_membership_notification_mailer.rb` -- email template rendering and delivery
- **Model layer**: `app/models/context_notification.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/notification.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/notification_subscription.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/users/notification_setting.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/welcome_notification.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/audit/notification.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: validates a unique user_id according to the correct scope

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates a unique user_id according to the correct scope

### S-2: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-3: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-4: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-5: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-6: sets the notified_at column

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the notified_at column

### S-7: does not enqueue a notification job

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not enqueue a notification job

### S-8: creates a notification belonging to the person being followed

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification belonging to the person being followed

### S-9: sends as perform_in 60 minutes if follower is new

- **Given** follower is new
- **When** the action is triggered
- **Then** sends as perform_in 60 minutes

### S-10: sends as perform_async if follower is not new

- **Given** follower is not new
- **When** the action is triggered
- **Then** sends as perform_async

### S-11: creates a notification from the follow instance

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification from the follow instance

### S-12: creates a notification belonging to the organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification belonging to the organization

