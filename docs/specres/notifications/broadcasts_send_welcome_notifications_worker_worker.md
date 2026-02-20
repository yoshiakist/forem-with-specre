---
id: "01KHY7Q07Y5HYVG6G55X6FC1Y7"
name: "broadcasts_send_welcome_notifications_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/broadcasts/send_welcome_notifications_worker.rb
- app/services/broadcasts/welcome_notification/generator.rb
- spec/workers/broadcasts/send_welcome_notifications_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Broadcasts::SendWelcomeNotificationsWorker` within the notifications domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/broadcasts/send_welcome_notifications_worker.rb` -- asynchronous job processing
- **Service layer**: `app/services/broadcasts/welcome_notification/generator.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: does nothing if Settings::General.welcome_notifications_live_at is nil

- **Given** Settings::General.welcome_notifications_live_at is nil
- **When** the action is triggered
- **Then** does nothing

### S-2: sends welcome notifications to new users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends welcome notifications to new users

