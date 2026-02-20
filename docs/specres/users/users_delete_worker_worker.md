---
id: "01KHY7Q04JC2RDR7C29CTZPSV8"
name: "users_delete_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/users/delete_worker.rb
- app/controllers/admin/users_controller.rb
- app/controllers/api/v0/admin/users_controller.rb
- app/controllers/api/v0/users_controller.rb
- app/controllers/api/v1/admin/users_controller.rb
- app/controllers/api/v1/users_controller.rb
- app/controllers/concerns/api/admin/users_controller.rb
- app/controllers/concerns/api/users_controller.rb
- app/controllers/users/notification_settings_controller.rb
- app/controllers/users/settings_controller.rb
- app/controllers/users_controller.rb
- spec/workers/users/delete_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::DeleteWorker` within the users domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **when user is found**: deletes the user correctly
- **when user is not found**: deletes the user correctly

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/users/delete_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/notification_settings_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/settings_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: deletes the user correctly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes the user correctly

### S-2: calls the service when a user is found

- **Given** the system is in a standard operational state
- **When** a user is found
- **Then** calls the service

### S-3: sends the notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends the notification

### S-4: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-5: sends the correct notification

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends the correct notification

### S-6: creates a gdpr-delete record

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a gdpr-delete record

### S-7: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-8: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

