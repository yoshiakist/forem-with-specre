---
id: "01KHY7Q062XTC6KD3HC0ZC54CC"
name: "audit_notification_service"
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
- spec/services/audit/notification_spec.rb

## Functional Overview

This specification defines the expected behavior of `Audit::Notification` within the notifications domain.

### Behavioral Areas

- **Publishing and receiving events**: Ensures correct behavior under the specified conditions
- **when payload is missing**: Ensures correct behavior under the specified conditions
- **when payload is present**: Ensures correct behavior under the specified conditions
- **Saving to database**: Ensures correct behavior under the specified conditions

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

### S-1: event is not created

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** event is not created

### S-2: receives an event

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** receives an event

### S-3: creates an AuditLog record

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an AuditLog record

