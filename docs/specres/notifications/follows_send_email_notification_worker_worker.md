---
id: "01KHY7Q080SHJJD22F8AS1ENYW"
name: "follows_send_email_notification_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/badge_achievements/send_email_notification_worker.rb
- app/workers/comments/send_email_notification_worker.rb
- app/workers/follows/send_email_notification_worker.rb
- app/workers/mentions/send_email_notification_worker.rb
- spec/workers/follows/send_email_notification_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Follows::SendEmailNotificationWorker` within the notifications domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **with follow**: sends a new_follower_email
- **without follow**: sends a new_follower_email

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/badge_achievements/send_email_notification_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/comments/send_email_notification_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/follows/send_email_notification_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/mentions/send_email_notification_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: sends a new_follower_email

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends a new_follower_email

### S-2: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-3: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-4: does not break

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not break

