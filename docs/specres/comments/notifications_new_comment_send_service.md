---
id: "01KHY7PZR3V05AYG4MVFM9XW5V"
name: "notifications_new_comment_send_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/notifications/new_comment/send.rb
- app/workers/comments/send_email_notification_worker.rb
- spec/services/notifications/new_comment/send_spec.rb

## Functional Overview

This specification defines the expected behavior of `Notifications::NewComment::Send` within the comments domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/notifications/new_comment/send.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/comments/send_email_notification_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: creates users notifications

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates users notifications

### S-2: creates a correct user notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a correct user notification

### S-3: does not send if comment has negative score already

- **Given** comment has negative score already
- **When** the action is triggered
- **Then** does not send

### S-4: creates the correct comment data for the notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates the correct comment data for the notification

### S-5: creates notifications for the article author and the parent comment author

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates notifications for the article author and the parent comment author

### S-6: creates notifications for all subscribed users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates notifications for all subscribed users

### S-7: creates author comments notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates author comments notification

### S-8: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-9: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-10: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-11: creates an organization notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an organization notification

### S-12: properly filters users for sending mobile push notifications

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** properly filters users for sending mobile push notifications

