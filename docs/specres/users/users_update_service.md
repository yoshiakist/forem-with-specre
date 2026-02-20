---
id: "01KHY7Q0063D2JGDEQPA0PDFGP"
name: "users_update_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/users/update.rb
- app/workers/users/update_user_activities_worker.rb
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
- spec/services/users/update_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::Update` within the users domain.

### Behavioral Areas

- **when changing username**: sets old_username and old_old_username when username was changed
- **when conditionally resaving articles**: sets old_username and old_old_username when username was changed

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/users/update.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/users/update_user_activities_worker.rb` -- asynchronous job processing
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

### S-1: automatically creates a profile for a user if it does not exist

- **Given** it does not exist
- **When** the action is triggered
- **Then** automatically creates a profile for a user

### S-2: correctly typecasts new attributes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** correctly typecasts new attributes

### S-3: removes old attributes from the profile

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes old attributes from the profile

### S-4: propagates changes to user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** propagates changes to user

### S-5: updates the profile_updated_at column

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the profile_updated_at column

### S-6: returns an error if Profile image is too large

- **Given** Profile image is too large
- **When** the action is triggered
- **Then** returns an error

### S-7: returns an error if Profile image is not a file

- **Given** Profile image is not a file
- **When** the action is triggered
- **Then** returns an error

### S-8: returns an error if Profile image file name is too long

- **Given** Profile image file name is too long
- **When** the action is triggered
- **Then** returns an error

### S-9: sets old_username and old_old_username when username was changed

- **Given** the system is in a standard operational state
- **When** username was changed
- **Then** sets old_username and old_old_username

### S-10: changes user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** changes user

### S-11: sets the correct article path when its slug contains username

- **Given** the system is in a standard operational state
- **When** its slug contains username
- **Then** sets the correct article path

### S-12: enqueues resave articles job when changing username

- **Given** the system is in a standard operational state
- **When** changing username
- **Then** enqueues resave articles job

