---
id: "01KHY7Q07R8Q581NJRBAADJ22A"
name: "notifications_notifications_page_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/notifications/counts_controller.rb
- app/controllers/notifications/reads_controller.rb
- app/controllers/notifications_controller.rb
- app/helpers/notifications_helper.rb
- app/services/notifications.rb
- app/services/notifications/milestone/send.rb
- app/services/notifications/moderation/send.rb
- app/services/notifications/new_badge_achievement/send.rb
- app/services/notifications/new_comment/send.rb
- app/services/notifications/new_follower/follow_data.rb
- spec/system/notifications/notifications_page_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Notifications` within the notifications domain.

### Behavioral Areas

- **Notifications page**: /notifications
- **when user is trusted**: allows trusted user to moderate content
- **with welcome notifications**: /notifications
- **without tracking enabled**: Ensures correct behavior under the specified conditions
- **with tracking enabled**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/notifications/counts_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/notifications/reads_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/notifications_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/notifications_helper.rb` -- shared view utility methods
- **Service layer**: `app/services/notifications.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/milestone/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/moderation/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/new_badge_achievement/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/new_comment/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/new_follower/follow_data.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: shows 1 notification and disappear after clicking it

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows 1 notification and disappear after clicking it

### S-2: /

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /

### S-3: allows trusted user to moderate content

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows trusted user to moderate content

### S-4: /notifications

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /notifications

### S-5: renders the notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the notification

### S-6: /notifications

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /notifications

### S-7: does not track events

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not track events

### S-8: /notifications

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /notifications

### S-9: tracks events

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** tracks events

### S-10: /notifications

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /notifications

