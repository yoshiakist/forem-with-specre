---
id: "01KHY7Q0J4YTDM07XMHAN52B4B"
name: "organizations_update_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/organization_memberships_controller.rb
- app/controllers/admin/organizations_controller.rb
- app/controllers/api/v0/organizations_controller.rb
- app/controllers/api/v1/organizations_controller.rb
- app/controllers/concerns/api/organizations_controller.rb
- app/controllers/organizations_controller.rb
- spec/requests/organizations_update_spec.rb

## Functional Overview

This specification defines the expected behavior of `"OrganizationsUpdate"` within the organizations domain.

### Behavioral Areas

- **OrganizationsUpdate**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/organization_memberships_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/organizations_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: updates org color with proper params

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates org color with proper params

### S-2: generates new secret

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** generates new secret

### S-3: updates profile_updated_at

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates profile_updated_at

### S-4: returns not_found if organization is missing

- **Given** organization is missing
- **When** the action is triggered
- **Then** returns not_found

### S-5: returns error if profile image file name is too long

- **Given** profile image file name is too long
- **When** the action is triggered
- **Then** returns error

### S-6: returns error if profile image is not a file

- **Given** profile image is not a file
- **When** the action is triggered
- **Then** returns error

