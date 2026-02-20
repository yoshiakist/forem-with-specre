---
id: "01KHY7Q0PVG6CWBAE5E8XG24VZ"
name: "follows_check_cached_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/follows/check_cached.rb
- app/controllers/api/v0/follows_controller.rb
- app/controllers/api/v1/follows_controller.rb
- app/controllers/concerns/api/follows_controller.rb
- app/controllers/follows_controller.rb
- app/services/follows/delete_cached.rb
- app/workers/follows/send_email_notification_worker.rb
- app/workers/follows/update_points_worker.rb
- spec/services/follows/check_cached_spec.rb

## Functional Overview

This specification defines the expected behavior of `Follows::CheckCached` within the follows domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/follows/check_cached.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/api/v0/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/follows_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/follows_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/follows/delete_cached.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/follows/send_email_notification_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/follows/update_points_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: checks if following a thing and returns true if they are

- **Given** following a thing and returns true if they are
- **When** the action is triggered
- **Then** checks

### S-2: checks if following a thing and returns false if they are not

- **Given** following a thing and returns false if they are not
- **When** the action is triggered
- **Then** checks

