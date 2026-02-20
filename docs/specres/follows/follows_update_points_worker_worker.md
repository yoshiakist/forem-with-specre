---
id: "01KHY7Q0PYE10S6DAR5CSNFYB2"
name: "follows_update_points_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/follows/update_points_worker.rb
- app/controllers/api/v0/follows_controller.rb
- app/controllers/api/v1/follows_controller.rb
- app/controllers/concerns/api/follows_controller.rb
- app/controllers/follows_controller.rb
- app/services/follows/check_cached.rb
- app/services/follows/delete_cached.rb
- app/workers/follows/send_email_notification_worker.rb
- spec/workers/follows/update_points_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Follows::UpdatePointsWorker` within the follows domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/follows/update_points_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/api/v0/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/follows_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/follows/check_cached.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/follows/delete_cached.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/follows/send_email_notification_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: calculates scores

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calculates scores

### S-2: has higher score with more long page views

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** has higher score with more long page views

### S-3: has higher score with more reactions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** has higher score with more reactions

### S-4: bumps down tag follow points not included in this calc

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** bumps down tag follow points not included in this calc

### S-5: applies inverse bonus to slightly penalize more popular tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** applies inverse bonus to slightly penalize more popular tags

