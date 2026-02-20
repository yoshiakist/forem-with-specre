---
id: "01KHY7Q03G9VV0QA2DHGMHKN52"
name: "user_views_logo_system"
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
- spec/system/user_views_logo_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Logo` within the users domain.

### Behavioral Areas

- **Logo behaviour**: renders the resized_logo
- **with an image set**: Ensures correct behavior under the specified conditions
- **without an image set**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: renders the resized_logo

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the resized_logo

### S-2: renders the the community name

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the the community name

