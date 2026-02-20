---
id: "01KHY7Q04QRSQZ9HE4N9ZBJ2F3"
name: "users_generate_ai_profile_image_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/users/generate_ai_profile_image_worker.rb
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
- spec/workers/users/generate_ai_profile_image_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::GenerateAiProfileImageWorker` within the users domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **when user cannot be found**: sets the remote profile image and saves the user
- **when image generation succeeds**: does not attempt to generate an image
- **when image generation does not return a url**: does not attempt to generate an image

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/users/generate_ai_profile_image_worker.rb` -- asynchronous job processing
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

### S-1: does not attempt to generate an image

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not attempt to generate an image

### S-2: sets the remote profile image and saves the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the remote profile image and saves the user

### S-3: includes aesthetic instructions when available

- **Given** the system is in a standard operational state
- **When** available
- **Then** includes aesthetic instructions

### S-4: falls back to default subforem aesthetic instructions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** falls back to default subforem aesthetic instructions

### S-5: does not attempt to update the profile image

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not attempt to update the profile image

