---
id: "01KHY7PZS588MXWFGM67CZ0GT3"
name: "comments_bust_cache_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/comments/bust_cache_worker.rb
- app/controllers/admin/comments_controller.rb
- app/controllers/api/v0/comments_controller.rb
- app/controllers/api/v1/comments_controller.rb
- app/controllers/comments_controller.rb
- app/controllers/concerns/api/comments_controller.rb
- app/helpers/comments_helper.rb
- app/queries/comments/community_wellness_query.rb
- app/queries/comments/count.rb
- app/queries/comments/tree.rb
- app/services/comments/calculate_score.rb
- spec/workers/comments/bust_cache_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Comments::BustCacheWorker` within the comments domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **with comment**: does not call purge on comment when commentable is not available
- **without comment**: does not call purge on comment when commentable is not available

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/comments/bust_cache_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/comments_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/comments_helper.rb` -- shared view utility methods
- **Query object**: `app/queries/comments/community_wellness_query.rb` -- complex database query encapsulation
- **Query object**: `app/queries/comments/count.rb` -- complex database query encapsulation
- **Query object**: `app/queries/comments/tree.rb` -- complex database query encapsulation
- **Service layer**: `app/services/comments/calculate_score.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: does not call purge on comment when commentable is not available

- **Given** the system is in a standard operational state
- **When** commentable is not available
- **Then** does not call purge on comment

### S-2: does not call purge on commentable when commentable is not available

- **Given** the system is in a standard operational state
- **When** commentable is not available
- **Then** does not call purge on commentable

### S-3: does not break

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not break

