---
id: "01KHY7Q07PWP033MCF65E86DF3"
name: "link_for_tags_in_posts_in_notifications_system"
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
- spec/system/link_for_tags_in_posts_in_notifications_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Link` within the notifications domain.

### Behavioral Areas

- **Link on tags for post in notifications**: Ensures correct behavior under the specified conditions
- **when user hasn**: Ensures correct behavior under the specified conditions
- **when logged in user**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/notification_subscriptions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/notifications/counts_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/notifications/reads_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/notifications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/notification_settings_controller.rb` -- HTTP request routing and response handling
- **Decorator**: `app/decorators/notification_decorator.rb` -- presentation logic and view-model enrichment


## Scenarios

### S-1: /dashboard

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /dashboard

### S-2: shows the sign-with page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the sign-with page

### S-3: shows articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows articles

### S-4: /dashboard

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /dashboard

