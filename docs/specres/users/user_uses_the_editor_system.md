---
id: "01KHY7Q03BNXF57J2PK5CZG4ZD"
name: "user_uses_the_editor_system"
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
- spec/system/user_uses_the_editor_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Using` within the users domain.

### Behavioral Areas

- **Using the editor**: Ensures correct behavior under the specified conditions
- **Viewing the editor**: Ensures correct behavior under the specified conditions
- **Previewing an article**: user write and publish an article
- **Submitting an article with v1 editor**: fills out form with rich content and click preview
- **without a title**: shows a message that the title cannot be blank
- **using v2 editor**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: /new

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /new

### S-2: renders the logo or Community name as expected

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the logo or Community name as expected

### S-3: /new

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /new

### S-4: fills out form with rich content and click preview

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** fills out form with rich content and click preview

### S-5: fill out form and submit

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** fill out form and submit

### S-6: user write and publish an article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** user write and publish an article

### S-7: shows a message that the title cannot be blank

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows a message that the title cannot be blank

### S-8: fill out form with rich content and click publish

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** fill out form with rich content and click publish

### S-9: /new

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /new

