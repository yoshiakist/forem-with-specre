---
id: "01KHY7Q0CA70A6FGB4RYB91QYD"
name: "tags_bust_cache_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/tags/bust_cache_worker.rb
- app/controllers/admin/tags/moderators_controller.rb
- app/controllers/admin/tags_controller.rb
- app/controllers/api/v0/tags_controller.rb
- app/controllers/api/v1/tags_controller.rb
- app/controllers/concerns/api/tags_controller.rb
- app/controllers/liquid_tags_controller.rb
- app/controllers/tags_controller.rb
- app/queries/tags/suggested_for_onboarding.rb
- app/workers/tags/alias_retag_worker.rb
- app/workers/tags/resave_supported_tags_worker.rb
- spec/workers/tags/bust_cache_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Tags::BustCacheWorker` within the tags domain.

### Behavioral Areas

- **perform_now**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/tags/bust_cache_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/tags/moderators_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/liquid_tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/tags_controller.rb` -- HTTP request routing and response handling
- **Query object**: `app/queries/tags/suggested_for_onboarding.rb` -- complex database query encapsulation
- **Background worker**: `app/workers/tags/alias_retag_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/tags/resave_supported_tags_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: busts cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts cache

### S-2: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

