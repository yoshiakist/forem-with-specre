---
id: "01KHY7Q0JC3KKP04SZJZN017ET"
name: "organizations_delete_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/organizations/delete.rb
- app/workers/organizations/delete_worker.rb
- app/controllers/admin/organizations_controller.rb
- app/controllers/api/v0/organizations_controller.rb
- app/controllers/api/v1/organizations_controller.rb
- app/controllers/concerns/api/organizations_controller.rb
- app/controllers/organizations_controller.rb
- app/helpers/admin/organizations_helper.rb
- app/queries/organizations/suggest_prominent.rb
- app/workers/organizations/bust_cache_worker.rb
- app/workers/organizations/save_article_worker.rb
- app/workers/organizations/track_promotional_billboard_impressions_worker.rb
- spec/services/organizations/delete_spec.rb

## Functional Overview

This specification defines the expected behavior of `Organizations::Delete` within the organizations domain.

### Behavioral Areas

- **with articles**: syncs articles

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/organizations/delete.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/organizations/delete_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/organizations_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/admin/organizations_helper.rb` -- shared view utility methods
- **Query object**: `app/queries/organizations/suggest_prominent.rb` -- complex database query encapsulation
- **Background worker**: `app/workers/organizations/bust_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/organizations/save_article_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/organizations/track_promotional_billboard_impressions_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: deletes an organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes an organization

### S-2: deletes notifications

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes notifications

### S-3: syncs articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** syncs articles

### S-4: removes the organization name from the .reading_list_document after destroy

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes the organization name from the .reading_list_document after destroy

