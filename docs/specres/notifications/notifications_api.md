---
id: "01KHY7Q05ZA0234CZQYGAJEDCF"
name: "notifications_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/notifications_controller.rb
- app/helpers/notifications_helper.rb
- app/services/notifications.rb
- app/workers/broadcasts/send_welcome_notifications_worker.rb
- app/workers/metrics/record_daily_notifications_worker.rb
- app/workers/notifications/create_round_robin_moderation_notifications_worker.rb
- app/workers/notifications/remove_old_notifications_worker.rb
- spec/requests/notifications_spec.rb

## Functional Overview

This specification defines the expected behavior of `"NotificationsIndex"` within the notifications domain.

### Behavioral Areas

- **NotificationsIndex**: Ensures correct behavior under the specified conditions
- **GET /notifications**: Ensures correct behavior under the specified conditions
- **when signed out**: Ensures correct behavior under the specified conditions
- **when signed in**: Ensures correct behavior under the specified conditions
- **when a user has new follow notifications**: renders the proper message for two notifications in the same day
- **when a user**: renders the correct user for a single reaction
- **when a user has new reaction notifications**: renders the proper message for two notifications in the same day
- **when a user**: renders the correct user for a single reaction

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/notifications_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/notifications_helper.rb` -- shared view utility methods
- **Service layer**: `app/services/notifications.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/broadcasts/send_welcome_notifications_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/metrics/record_daily_notifications_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/notifications/create_round_robin_moderation_notifications_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/notifications/remove_old_notifications_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: renders page with the proper heading

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders page with the proper heading

### S-2: renders the signin page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the signin page

### S-3: does not render the signup cue

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not render the signup cue

### S-4: renders the proper message for a single notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper message for a single notification

### S-5: renders the proper message for two notifications in the same day

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper message for two notifications in the same day

### S-6: renders the proper message for three or more notifications in the same day

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper message for three or more notifications in the same day

### S-7: does group notifications that occur on different days

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** does group notifications that occur on different days

### S-8: renders the proper message for a single notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper message for a single notification

### S-9: renders the proper message for two notifications in the same day

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper message for two notifications in the same day

### S-10: renders the proper message for three or more notifications in the same day

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper message for three or more notifications in the same day

### S-11: does group notifications that occur on different days

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** does group notifications that occur on different days

### S-12: does not render the proper message for a single notification if missing :org_id

- **Given** missing :org_id
- **When** the action is triggered
- **Then** does not render the proper message for a single notification

