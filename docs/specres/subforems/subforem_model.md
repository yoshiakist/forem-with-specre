---
id: "01KHY7Q1B6HR02XD4GXRBWMTW3"
name: "subforem_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/subforems_controller.rb
- app/controllers/api/v0/subforems_controller.rb
- app/controllers/api/v1/subforems_controller.rb
- app/controllers/concerns/api/subforems_controller.rb
- app/controllers/subforems_controller.rb
- app/lib/middlewares/set_subforem.rb
- app/models/subforem.rb
- app/models/tag_subforem_relationship.rb
- app/policies/subforem_policy.rb
- app/services/ai/subforem_finder.rb
- app/services/images/generate_subforem_images.rb
- app/services/subforem_reassignment_service.rb
- app/uploaders/subforem_image_uploader.rb
- app/workers/notifications/subforem_change_notification_worker.rb
- spec/models/subforem_spec.rb

## Functional Overview

This specification defines the expected behavior of `Subforem` within the subforems domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **misc subforem functionality**: calls subforem_default_idods after save
- **.create_from_scratch!**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/subforems_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/subforems_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/subforems_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/subforems_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/subforems_controller.rb` -- HTTP request routing and response handling
- `app/lib/middlewares/set_subforem.rb`
- **Model layer**: `app/models/subforem.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/tag_subforem_relationship.rb` -- data persistence, validations, and associations
- **Policy layer**: `app/policies/subforem_policy.rb` -- authorization and access control rules
- **Service layer**: `app/services/ai/subforem_finder.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/images/generate_subforem_images.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/subforem_reassignment_service.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: calls subforem_default_idods after save

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls subforem_default_idods after save

### S-2: downcases domain before validation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** downcases domain before validation

### S-3: calculates score and hotness_score correctly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calculates score and hotness_score correctly

### S-4: finds misc subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** finds misc subforem

### S-5: returns nil when no misc subforem exists

- **Given** the system is in a standard operational state
- **When** no misc subforem exists
- **Then** returns nil

### S-6: busts misc subforem cache when subforem is updated

- **Given** the system is in a standard operational state
- **When** subforem is updated
- **Then** busts misc subforem cache

### S-7: creates a subforem and queues background job

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a subforem and queues background job

### S-8: works without background image URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** works without background image URL

### S-9: returns the created subforem

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the created subforem

