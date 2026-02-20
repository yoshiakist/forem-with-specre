---
id: "01KHY7Q1BZZ7H0D1JE70529GT4"
name: "subforems_create_from_scratch_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/subforems/create_from_scratch_worker.rb
- app/controllers/admin/subforems_controller.rb
- app/controllers/api/v0/subforems_controller.rb
- app/controllers/api/v1/subforems_controller.rb
- app/controllers/concerns/api/subforems_controller.rb
- app/controllers/subforems_controller.rb
- spec/workers/subforems/create_from_scratch_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Subforems::CreateFromScratchWorker` within the subforems domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **when an error occurs**: logs error and re-raises
- **when subforem does not exist**: sets up the subforem with all AI services

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/subforems/create_from_scratch_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/subforems_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/subforems_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/subforems_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/subforems_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/subforems_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: sets up the subforem with all AI services

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets up the subforem with all AI services

### S-2: works without background image URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** works without background image URL

### S-3: logs success message

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs success message

### S-4: logs error and re-raises

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs error and re-raises

### S-5: raises an error

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises an error

