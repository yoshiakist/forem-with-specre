---
id: "01KHY7Q0JHDTCY43PWT6X6XGBJ"
name: "organizations_bust_cache_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/organizations/bust_cache_worker.rb
- app/controllers/admin/organizations_controller.rb
- app/controllers/api/v0/organizations_controller.rb
- app/controllers/api/v1/organizations_controller.rb
- app/controllers/concerns/api/organizations_controller.rb
- app/controllers/organizations_controller.rb
- app/helpers/admin/organizations_helper.rb
- app/queries/organizations/suggest_prominent.rb
- app/services/organizations/delete.rb
- app/workers/organizations/delete_worker.rb
- app/workers/organizations/save_article_worker.rb
- spec/workers/organizations/bust_cache_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Organizations::BustCacheWorker` within the organizations domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **when no organization is found**: Ensures correct behavior under the specified conditions
- **when no slug is found**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/organizations/bust_cache_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/organizations_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/admin/organizations_helper.rb` -- shared view utility methods
- **Query object**: `app/queries/organizations/suggest_prominent.rb` -- complex database query encapsulation
- **Service layer**: `app/services/organizations/delete.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/organizations/delete_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/organizations/save_article_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: doest not call the service

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doest not call the service

### S-2: doest not call the service

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doest not call the service

### S-3: busts cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts cache

