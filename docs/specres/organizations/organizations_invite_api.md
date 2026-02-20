---
id: "01KHY7Q0HZNMZR9K9FWD0VAD7M"
name: "organizations_invite_api"
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
- spec/requests/organizations_invite_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Organizations` within the organizations domain.

### Behavioral Areas

- **Organizations Invite**: Ensures correct behavior under the specified conditions
- **POST /organizations/:id/invite**: Ensures correct behavior under the specified conditions
- **when organization is not fully trusted**: creates a membership even when limits would normally be exceeded
- **when organization is fully trusted**: creates a membership even when limits would normally be exceeded
- **when user is not found**: handles username with @ symbol
- **when user is already a member**: creates a pending membership
- **when user already has a pending invitation**: creates a pending membership
- **when user is not authorized**: handles username with @ symbol

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/organization_memberships_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/organizations_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: creates a pending membership

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a pending membership

### S-2: sends an invitation email

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends an invitation email

### S-3: redirects with success message

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects with success message

### S-4: handles username with @ symbol

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles username with @ symbol

### S-5: handles username with whitespace

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles username with whitespace

### S-6: creates an active membership (not pending)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an active membership (not pending)

### S-7: sends a notification email (not invitation)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends a notification email (not invitation)

### S-8: does not send an invitation email

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not send an invitation email

### S-9: redirects with success message

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects with success message

### S-10: redirects with error message

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects with error message

### S-11: does not create a new membership

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create a new membership

### S-12: redirects with error message

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects with error message

