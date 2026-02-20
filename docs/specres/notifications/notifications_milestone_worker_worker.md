---
id: "01KHY7Q08G1J489W4M0M6WGQET"
name: "notifications_milestone_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/notifications/milestone_worker.rb
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
- spec/workers/notifications/milestone_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Notifications::MilestoneWorker` within the notifications domain.

### Behavioral Areas

- **perform_now**: Ensures correct behavior under the specified conditions
- **When it does not find article from id**: does not call the service
- **When finds article from id**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/notifications/milestone_worker.rb` -- asynchronous job processing
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

### S-1: does not call the service

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call the service

### S-2: calls the service

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls the service

