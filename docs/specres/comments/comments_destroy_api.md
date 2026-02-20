---
id: "01KHY7PZQ220A5V7ZZVY5Y2SFR"
name: "comments_destroy_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/comments_controller.rb
- app/controllers/api/v0/comments_controller.rb
- app/controllers/api/v1/comments_controller.rb
- app/controllers/comments_controller.rb
- app/controllers/concerns/api/comments_controller.rb
- app/controllers/discussion_locks_controller.rb
- spec/requests/comments_destroy_spec.rb

## Functional Overview

This specification defines the expected behavior of `"CommentsDestroy"` within the comments domain.

### Behavioral Areas

- **CommentsDestroy**: Ensures correct behavior under the specified conditions
- **GET /:username/comment/:id_code/delete_confirm**: Ensures correct behavior under the specified conditions
- **DELETE /comments/:id**: marks the comment as deleted
- **when comment has no children**: destroys the comment
- **when comment has children**: destroys the comment

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/discussion_locks_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: renders the confirmation message

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the confirmation message

### S-2: destroys the comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** destroys the comment

### S-3: marks the comment as deleted

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** marks the comment as deleted

### S-4: renders [deleted]

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders [deleted]

