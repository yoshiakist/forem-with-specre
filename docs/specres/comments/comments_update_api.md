---
id: "01KHY7PZQ73591KW17N1TN8D7T"
name: "comments_update_api"
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
- spec/requests/comments_update_spec.rb

## Functional Overview

This specification defines the expected behavior of `"CommentsUpdate"` within the comments domain.

### Behavioral Areas

- **CommentsUpdate**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/discussion_locks_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: updates ordinary article with proper params

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates ordinary article with proper params

### S-2: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

