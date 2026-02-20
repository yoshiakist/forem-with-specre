---
id: "01KHY7Q0M2XYKB60B8K72BG86J"
name: "profiles_request_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/profile_field_groups_controller.rb
- app/controllers/admin/profile_fields_controller.rb
- app/controllers/api/v0/profile_images_controller.rb
- app/controllers/api/v1/profile_images_controller.rb
- app/controllers/concerns/api/profile_images_controller.rb
- app/controllers/profile_field_groups_controller.rb
- spec/requests/profiles_request_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Profiles"` within the profiles domain.

### Behavioral Areas

- **Profiles**: Ensures correct behavior under the specified conditions
- **POST /profiles**: Ensures correct behavior under the specified conditions
- **when signed out**: Ensures correct behavior under the specified conditions
- **when signed in**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/profile_field_groups_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/profile_fields_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/profile_field_groups_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: redirects to the login page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to the login page

### S-2: updates the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the user

### S-3: updates the profile

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the profile

