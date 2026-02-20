---
id: "01KHY7PZRB4XTPSHBFX4N9XZHS"
name: "users_delete_comments_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/users/delete_comments.rb
- spec/services/users/delete_comments_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::DeleteComments` within the comments domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/users/delete_comments.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: destroys user comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** destroys user comments

### S-2: busts cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts cache

### S-3: destroys moderation notifications properly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** destroys moderation notifications properly

