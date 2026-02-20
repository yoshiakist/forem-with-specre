---
id: "01KHY7Q020VDGHG86S7SP424G4"
name: "organization_user_leaves_an_organization_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/gdpr_delete_requests_controller.rb
- app/controllers/admin/settings/authentications_controller.rb
- app/controllers/admin/settings/user_experiences_controller.rb
- app/controllers/admin/user_queries_controller.rb
- app/controllers/admin/users_controller.rb
- app/controllers/api/v0/admin/users_controller.rb
- spec/system/organization/user_leaves_an_organization_spec.rb

## Functional Overview

This specification defines the expected behavior of `"User` within the users domain.

### Behavioral Areas

- **User leaves an organization**: /settings/organization/#{organization.id}
- **when user visits member organization settings**: /settings/organization/#{organization.id}
- **when user leaves member organization**: /settings/organization/#{organization.id}

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: /settings/organization/#{organization.id}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /settings/organization/#{organization.id}

### S-2: shows the leave organization button

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the leave organization button

### S-3: leaves organization and shows confirmation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** leaves organization and shows confirmation

