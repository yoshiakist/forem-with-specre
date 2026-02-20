---
id: "01KHY7Q0KRV1JNTSJEVZ1VZWEC"
name: "api_v1_profile_images_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/api/v0/profile_images_controller.rb
- app/controllers/api/v1/profile_images_controller.rb
- app/controllers/concerns/api/profile_images_controller.rb
- spec/requests/api/v1/profile_images_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Api::V1::ProfileImages"` within the profiles domain.

### Behavioral Areas

- **Api::V1::ProfileImages**: Ensures correct behavior under the specified conditions
- **GET /api/profile_images/:username**: Ensures correct behavior under the specified conditions
- **when the username relates to an user**: returns 404 if the username is not taken
- **when the username relates to an invited user**: returns 404 if the username is not taken
- **when the username relates to an organization**: returns 404 if the username is not taken

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/api/v0/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/profile_images_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns 404 if the username is not taken

- **Given** the username is not taken
- **When** the action is triggered
- **Then** returns 404

### S-2: returns the user profile image information

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the user profile image information

### S-3: returns a 404

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a 404

### S-4: returns the organization

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the organization

