---
id: "01KHY7Q022QGVYZATSYQ81S49M"
name: "organization_user_updates_org_settings_system"
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
- spec/system/organization/user_updates_org_settings_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Organization` within the users domain.

### Behavioral Areas

- **Organization setting page(/settings/organization)**: user creates an organization

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: user creates an organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** user creates an organization

### S-2: /settings/organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /settings/organization

### S-3: promotes a member to an admin

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** promotes a member to an admin

### S-4: /settings/organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /settings/organization

### S-5: revokes an admin

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** revokes an admin

### S-6: /settings/organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /settings/organization

### S-7: remove user from organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** remove user from organization

### S-8: /settings/organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /settings/organization

### S-9: uses the update page when an update error occurs

- **Given** the system is in a standard operational state
- **When** an update error occurs
- **Then** uses the update page

### S-10: /settings/organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /settings/organization

