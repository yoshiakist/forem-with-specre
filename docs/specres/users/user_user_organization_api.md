---
id: "01KHY7PZWWK69G6BPBTYMEHACF"
name: "user_user_organization_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/settings/user_experiences_controller.rb
- app/controllers/admin/user_queries_controller.rb
- app/controllers/admin/users_controller.rb
- app/controllers/api/v0/admin/users_controller.rb
- app/controllers/api/v0/users_controller.rb
- app/controllers/api/v1/admin/users_controller.rb
- app/controllers/api/v1/user_roles_controller.rb
- app/controllers/api/v1/users_controller.rb
- app/controllers/concerns/api/admin/users_controller.rb
- app/controllers/concerns/api/users_controller.rb
- spec/requests/user/user_organization_spec.rb

## Functional Overview

This specification defines the expected behavior of `"UserOrganization"` within the users domain.

### Behavioral Areas

- **UserOrganization**: Ensures correct behavior under the specified conditions
- **when joining an org**: redirects correctly when not scheduling
- **when creating a new org**: redirects correctly when not scheduling
- **when leaving an org**: redirects correctly when not scheduling
- **when adding an org admin**: adds org admin
- **when removing an org admin**: adds org admin
- **when deleting an organization**: creates an organization_membership association
- **when signed in as org_admin**: raises not_authorized if user is not org_admin

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/user_roles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: creates an organization_membership association

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an organization_membership association

### S-2: shows an error message if secret is invalid

- **Given** secret is invalid
- **When** the action is triggered
- **Then** shows an error message

### S-3: correctly strips the secret of the org_secret param

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** correctly strips the secret of the org_secret param

### S-4: creates the correct organization_membership association

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates the correct organization_membership association

### S-5: redirects to the proper org settings page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to the proper org settings page

### S-6: returns a too_many_requests response if the rate limit is reached

- **Given** the rate limit is reached
- **When** the action is triggered
- **Then** returns a too_many_requests response

### S-7: returns error if profile image file name is too long

- **Given** profile image file name is too long
- **When** the action is triggered
- **Then** returns error

### S-8: returns error if profile image is not a file

- **Given** profile image is not a file
- **When** the action is triggered
- **Then** returns error

### S-9: leaves org and deletes the member

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** leaves org and deletes the member

### S-10: adds org admin

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds org admin

### S-11: creates the org_membership association

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates the org_membership association

### S-12: raises not_authorized if user is not org_admin

- **Given** user is not org_admin
- **When** the action is triggered
- **Then** raises not_authorized

