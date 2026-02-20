---
id: "01KHY7Q065ZZNB2C293EQQVP8N"
name: "broadcasts_welcome_notification_generator_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/broadcasts/welcome_notification/generator.rb
- app/models/welcome_notification.rb
- app/services/notifications/welcome_notification/send.rb
- app/workers/broadcasts/send_welcome_notifications_worker.rb
- app/workers/notifications/welcome_notification_worker.rb
- spec/services/broadcasts/welcome_notification/generator_spec.rb

## Functional Overview

This specification defines the expected behavior of `Broadcasts::WelcomeNotification::Generator` within the notifications domain.

### Behavioral Areas

- **.call**: Ensures correct behavior under the specified conditions
- **send_welcome_notification**: Ensures correct behavior under the specified conditions
- **send_authentication_notification**: Ensures correct behavior under the specified conditions
- **send_feed_customization_notification**: Ensures correct behavior under the specified conditions
- **send_ux_customization_notification**: Ensures correct behavior under the specified conditions
- **send_discuss_and_ask_notification**: Ensures correct behavior under the specified conditions
- **with a user who has asked a question**: requires a valid user id
- **with a user who has started a discussion**: requires a valid user id

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/broadcasts/welcome_notification/generator.rb` -- business logic orchestration and domain operations
- **Model layer**: `app/models/welcome_notification.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/notifications/welcome_notification/send.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/broadcasts/send_welcome_notifications_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/notifications/welcome_notification_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: requires a valid user id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** requires a valid user id

### S-2: does not send a notification to an unsubscribed user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not send a notification to an unsubscribed user

### S-3: does not send a notification if no active broadcast exists

- **Given** no active broadcast exists
- **When** the action is triggered
- **Then** does not send a notification

### S-4: sends only 1 notification at a time, in the correct order

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends only 1 notification at a time, in the correct order

### S-5: does not send a notification to a newly-created user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not send a notification to a newly-created user

### S-6: generates the correct broadcast type and sends the notification to the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** generates the correct broadcast type and sends the notification to the user

### S-7: does not send to a user who has commented in a welcome thread

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not send to a user who has commented in a welcome thread

### S-8: does not send duplicate notifications

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not send duplicate notifications

### S-9: does not send notification if user is created less than a day ago

- **Given** user is created less than a day ago
- **When** the action is triggered
- **Then** does not send notification

### S-10: does not send notification if user is authenticated with both services

- **Given** user is authenticated with both services
- **When** the action is triggered
- **Then** does not send notification

### S-11: does not send notification if user is authenticated with all services

- **Given** user is authenticated with all services
- **When** the action is triggered
- **Then** does not send notification

### S-12: does not send duplicate notifications for #{provider_name}

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not send duplicate notifications for #{provider_name}

