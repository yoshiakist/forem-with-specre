---
id: "01KHY7Q07VDSBH7N10T7MY4JZ5"
name: "badge_achievements_send_email_notification_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/badge_achievements/send_email_notification_worker.rb
- app/workers/comments/send_email_notification_worker.rb
- app/workers/follows/send_email_notification_worker.rb
- app/workers/mentions/send_email_notification_worker.rb
- spec/workers/badge_achievements/send_email_notification_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `BadgeAchievements::SendEmailNotificationWorker` within the notifications domain.

### Behavioral Areas

- **perform_now**: Ensures correct behavior under the specified conditions
- **with badge achievement**: sends badge email
- **without badge achievement**: sends badge email

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/badge_achievements/send_email_notification_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/comments/send_email_notification_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/follows/send_email_notification_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/mentions/send_email_notification_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: sends badge email

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends badge email

### S-2: does not error

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not error

### S-3: does not call NotifyMailer

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call NotifyMailer

