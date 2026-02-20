---
id: "01KHY7Q1HEAS9THK32MYXFPPEK"
name: "mentions_create_all_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/mentions/create_all.rb
- app/workers/mentions/create_all_worker.rb
- app/workers/mentions/send_email_notification_worker.rb
- spec/services/mentions/create_all_spec.rb

## Functional Overview

This specification defines the expected behavior of `Mentions::CreateAll` within the mentions domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/mentions/create_all.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/mentions/create_all_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/mentions/send_email_notification_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: does not create mentions if a user is not mentioned

- **Given** a user is not mentioned
- **When** the action is triggered
- **Then** does not create mentions

### S-2: creates a mention if notifiable is updated to include mention

- **Given** notifiable is updated to include mention
- **When** the action is triggered
- **Then** creates a mention

### S-3: does not create a mention if notifiable is updated with mention inside code bloc...

- **Given** notifiable is updated with mention inside code block
- **When** the action is triggered
- **Then** does not create a mention

### S-4: does not create a mention if notifiable is updated with mention inside code snip...

- **Given** notifiable is updated with mention inside code snippet
- **When** the action is triggered
- **Then** does not create a mention

### S-5: does not create a mention if notifiable is updated liquid tag that would render ...

- **Given** notifiable is updated liquid tag that would render mention-like text
- **When** the action is triggered
- **Then** does not create a mention

### S-6: creates mention if there is a user mentioned and if the user doesn

- **Given** there is a user mentioned and if the user doesn
- **When** the action is triggered
- **Then** creates mention

### S-7: deletes mention if deleted from notifiable

- **Given** deleted from notifiable
- **When** the action is triggered
- **Then** deletes mention

### S-8: deletes notifications associated with mention if deleted from notifiable

- **Given** deleted from notifiable
- **When** the action is triggered
- **Then** deletes notifications associated with mention

### S-9: creates one mention even if multiple mentions of same user

- **Given** multiple mentions of same user
- **When** the action is triggered
- **Then** creates one mention even

### S-10: creates multiple mentions for multiple users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates multiple mentions for multiple users

### S-11: deletes one of multiple mentions if one of multiple is deleted

- **Given** one of multiple is deleted
- **When** the action is triggered
- **Then** deletes one of multiple mentions

### S-12: creates a mention on creation of notifiable

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a mention on creation of notifiable

