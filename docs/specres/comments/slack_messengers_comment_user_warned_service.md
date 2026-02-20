---
id: "01KHY7PZR9Z8S7DK0R6J561F73"
name: "slack_messengers_comment_user_warned_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/slack/messengers/comment_user_warned.rb
- spec/services/slack/messengers/comment_user_warned_spec.rb

## Functional Overview

This specification defines the expected behavior of `Slack::Messengers::CommentUserWarned` within the comments domain.

### Behavioral Areas

- **when the uesr has been warned**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/slack/messengers/comment_user_warned.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: does not message slack for a comment with a regular user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not message slack for a comment with a regular user

### S-2: contains the correct info

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** contains the correct info

### S-3: messages the proper channel with the proper username and emoji

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** messages the proper channel with the proper username and emoji

