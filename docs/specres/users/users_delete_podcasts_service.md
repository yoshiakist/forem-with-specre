---
id: "01KHY7PZZSFXY17VH1G33CANWN"
name: "users_delete_podcasts_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/users/delete_podcasts.rb
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
- spec/services/users/delete_podcasts_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::DeletePodcasts` within the users domain.

### Behavioral Areas

- **when podcast is owned by multiple users**: removes ownership from the given user and deletes the podcast
- **when podcast is owned by one user**: only removes ownership from the given user

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/users/delete_podcasts.rb` -- business logic orchestration and domain operations
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

### S-1: only removes ownership from the given user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** only removes ownership from the given user

### S-2: removes ownership from the given user and deletes the podcast

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes ownership from the given user and deletes the podcast

