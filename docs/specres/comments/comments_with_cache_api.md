---
id: "01KHY7PZQACGVB2ZM2Q3D54VQ4"
name: "comments_with_cache_api"
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
- spec/requests/comments_with_cache_spec.rb

## Functional Overview

This specification defines the expected behavior of `"ArticleCommentsWithCache"` within the comments domain.

### Behavioral Areas

- **ArticleCommentsWithCache**: Ensures correct behavior under the specified conditions
- **GET /:slug (articles)**: Ensures correct behavior under the specified conditions
- **GET /:username/comment/:id_code (root comment path)**: busts comments cache

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/discussion_locks_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: busts comments cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts comments cache

### S-2: busts cache when spam comment is a child and a parent

- **Given** the system is in a standard operational state
- **When** spam comment is a child and a parent
- **Then** busts cache

### S-3: busts cache for root comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts cache for root comment

