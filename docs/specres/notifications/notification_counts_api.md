---
id: "01KHY7Q05Q1XQ5BMCCPQXSGQK5"
name: "notification_counts_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/notification_subscriptions_controller.rb
- app/controllers/notifications/counts_controller.rb
- app/controllers/notifications/reads_controller.rb
- app/controllers/notifications_controller.rb
- app/controllers/users/notification_settings_controller.rb
- app/decorators/notification_decorator.rb
- spec/requests/notification_counts_spec.rb

## Functional Overview

This specification defines the expected behavior of `"NotificationCounts"` within the notifications domain.

### Behavioral Areas

- **NotificationCounts**: Ensures correct behavior under the specified conditions
- **GET /notifications/counts**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/notification_subscriptions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/notifications/counts_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/notifications/reads_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/notifications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/notification_settings_controller.rb` -- HTTP request routing and response handling
- **Decorator**: `app/decorators/notification_decorator.rb` -- presentation logic and view-model enrichment


## Scenarios

### S-1: returns count if signed in

- **Given** signed in
- **When** the action is triggered
- **Then** returns count

### S-2: returns 0 if no user is present

- **Given** no user is present
- **When** the action is triggered
- **Then** returns 0

