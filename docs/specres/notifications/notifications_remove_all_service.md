---
id: "01KHY7Q079FPR8SGF1FH9BKDTH"
name: "notifications_remove_all_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/notifications/remove_all.rb
- app/services/notifications/remove_all_by_action.rb
- app/workers/notifications/remove_all_worker.rb
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
- spec/services/notifications/remove_all_spec.rb

## Functional Overview

This specification defines the expected behavior of `Notifications::RemoveAll` within the notifications domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/notifications/remove_all.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/remove_all_by_action.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/notifications/remove_all_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/notifications/counts_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/notifications/reads_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/notifications_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/notifications_helper.rb` -- shared view utility methods
- **Service layer**: `app/services/notifications.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/milestone/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/moderation/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/new_badge_achievement/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/new_comment/send.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: checks all notifiables are deleted

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** checks all notifiables are deleted

