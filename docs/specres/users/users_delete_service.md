---
id: "01KHY7PZZW47GV0J3YP2DXFGHT"
name: "users_delete_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/gdpr_delete_requests_controller.rb
- app/models/gdpr_delete_request.rb
- app/models/users/deleted_user.rb
- app/queries/admin/gdpr_delete_requests_query.rb
- app/services/moderator/delete_user.rb
- app/services/segmented_users/bulk_delete.rb
- app/services/users/delete.rb
- app/services/users/delete_activity.rb
- app/services/users/delete_articles.rb
- app/services/users/delete_comments.rb
- app/services/users/delete_podcasts.rb
- app/workers/users/delete_worker.rb
- app/controllers/admin/users_controller.rb
- app/controllers/api/v0/admin/users_controller.rb
- app/controllers/api/v0/users_controller.rb
- spec/services/users/delete_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::Delete` within the users domain.

### Behavioral Areas

- **deleting associations**: keeps the kept associations
- **when the user was suspended**: deletes user
- **when the user was a spammer**: deletes user

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/gdpr_delete_request.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/users/deleted_user.rb` -- data persistence, validations, and associations
- **Query object**: `app/queries/admin/gdpr_delete_requests_query.rb` -- complex database query encapsulation
- **Service layer**: `app/services/moderator/delete_user.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/segmented_users/bulk_delete.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/delete.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/delete_activity.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/delete_articles.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/delete_comments.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/delete_podcasts.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/users/delete_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: deletes user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes user

### S-2: busts user profile page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts user profile page

### S-3: deletes user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes user

### S-4: deletes user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes user

### S-5: deletes user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes user

### S-6: deletes the destroy token

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes the destroy token

### S-7: does not delete user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not delete user

### S-8: deletes field tests memberships

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes field tests memberships

### S-9: deletes reactions to the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes reactions to the user

### S-10: keeps the kept associations

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** keeps the kept associations

### S-11: deletes all the associations

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes all the associations

### S-12: stores a hash of the username so the user can

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** stores a hash of the username so the user can

