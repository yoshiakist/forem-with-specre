---
id: "01KHY7Q0JM4WZWZGDGM1BTPW0F"
name: "organizations_delete_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/organizations/delete_worker.rb
- app/controllers/admin/organizations_controller.rb
- app/controllers/api/v0/organizations_controller.rb
- app/controllers/api/v1/organizations_controller.rb
- app/controllers/concerns/api/organizations_controller.rb
- app/controllers/organizations_controller.rb
- app/helpers/admin/organizations_helper.rb
- app/queries/organizations/suggest_prominent.rb
- app/services/organizations/delete.rb
- app/workers/organizations/bust_cache_worker.rb
- app/workers/organizations/save_article_worker.rb
- spec/workers/organizations/delete_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Organizations::DeleteWorker` within the organizations domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **when org and user are found**: touches the user
- **when update_and_notify_user is true**: Ensures correct behavior under the specified conditions
- **when an org or a user is not found**: touches the user

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/organizations/delete_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/organizations_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/admin/organizations_helper.rb` -- shared view utility methods
- **Query object**: `app/queries/organizations/suggest_prominent.rb` -- complex database query encapsulation
- **Service layer**: `app/services/organizations/delete.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/organizations/bust_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/organizations/save_article_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: destroys the org

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** destroys the org

### S-2: calls the service

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls the service

### S-3: creates an audit_log record

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an audit_log record

### S-4: creates a correct AuditLog record

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a correct AuditLog record

### S-5: touches the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** touches the user

### S-6: busts user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts user

### S-7: sends the notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends the notification

### S-8: sends the correct notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends the correct notification

### S-9: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-10: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-11: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

