---
id: "01KHY7Q03VR92VH9Y1C3HJAKQE"
name: "users_settings_view"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/users/notification_settings_controller.rb
- app/controllers/users/settings_controller.rb
- app/controllers/admin/users_controller.rb
- app/controllers/api/v0/admin/users_controller.rb
- app/controllers/api/v0/users_controller.rb
- app/controllers/api/v1/admin/users_controller.rb
- app/controllers/api/v1/users_controller.rb
- app/controllers/concerns/api/admin/users_controller.rb
- app/controllers/concerns/api/users_controller.rb
- app/controllers/users_controller.rb
- app/helpers/admin/users_helper.rb
- app/helpers/users_helper.rb
- spec/views/users/settings_spec.rb

## Functional Overview

This specification defines the expected behavior of `"users/edit"` within the users domain.

### Behavioral Areas

- **users/edit**: Ensures correct behavior under the specified conditions
- **/settings/organization**: Ensures correct behavior under the specified conditions
- **when the user is an org admin**: shows the org admin page

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/users/notification_settings_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/settings_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/admin/users_helper.rb` -- shared view utility methods
- **View helper**: `app/helpers/users_helper.rb` -- shared view utility methods


## Scenarios

### S-1: shows the org admin page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the org admin page

### S-2: shows the destroy button if the org has one admin and no content

- **Given** the org has one admin and no content
- **When** the action is triggered
- **Then** shows the destroy button

### S-3: shows the proper message if the org has more than one member

- **Given** the org has more than one member
- **When** the action is triggered
- **Then** shows the proper message

### S-4: shows the proper message if the org has an article

- **Given** the org has an article
- **When** the action is triggered
- **Then** shows the proper message

