---
id: "01KHY7Q0BVADZC20CBVMQ299VM"
name: "api_v1_tags_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/tags_controller.rb
- app/controllers/api/v0/tags_controller.rb
- app/controllers/api/v1/tags_controller.rb
- app/controllers/concerns/api/tags_controller.rb
- app/controllers/liquid_tags_controller.rb
- app/controllers/tags_controller.rb
- app/workers/tags/resave_supported_tags_worker.rb
- spec/requests/api/v1/tags_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Api::V1::Tags"` within the tags domain.

### Behavioral Areas

- **Api::V1::Tags**: Ensures correct behavior under the specified conditions
- **GET /api/tags**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/liquid_tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/tags_controller.rb` -- HTTP request routing and response handling
- **Background worker**: `app/workers/tags/resave_supported_tags_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: returns tags

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns tags

### S-2: returns tags with the correct json representation

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns tags with the correct json representation

### S-3: orders tags by taggings_count in a descending order

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** orders tags by taggings_count in a descending order

### S-4: supports pagination

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** supports pagination

### S-5: respects API_PER_PAGE_MAX limit set in ENV variable

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** respects API_PER_PAGE_MAX limit set in ENV variable

### S-6: sets the correct edge caching surrogate key for all tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the correct edge caching surrogate key for all tags

