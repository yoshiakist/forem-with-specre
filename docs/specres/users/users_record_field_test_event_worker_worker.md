---
id: "01KHY7Q04W1FW39XENG4MMVBQA"
name: "users_record_field_test_event_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/users/record_field_test_event_worker.rb
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
- spec/workers/users/record_field_test_event_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::RecordFieldTestEventWorker` within the users domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **with a non-existent user**: Ensures correct behavior under the specified conditions
- **with a user**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/users/record_field_test_event_worker.rb` -- asynchronous job processing
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

### S-1: gracefully exits

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** gracefully exits

### S-2: forward delegates to AbExperiment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** forward delegates to AbExperiment

