---
id: "01KHY7Q0KVMWQQ2DMHNVN6YRJH"
name: "profile_field_groups_request_api"
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
- spec/requests/profile_field_groups_request_spec.rb

## Functional Overview

This specification defines the expected behavior of `"ProfileFieldGroups"` within the profiles domain.

### Behavioral Areas

- **ProfileFieldGroups**: Ensures correct behavior under the specified conditions
- **GET /profile_field_groups**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/profile_field_groups_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/profile_fields_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/profile_field_groups_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns a successful response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a successful response

### S-2: returns all groups with all fields by default

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns all groups with all fields by default

### S-3: returns only groups with onboarding fields when onboarding=true

- **Given** the system is in a standard operational state
- **When** onboarding=true
- **Then** returns only groups with onboarding fields

### S-4: only returns the onboarding fields in the group

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** only returns the onboarding fields in the group

