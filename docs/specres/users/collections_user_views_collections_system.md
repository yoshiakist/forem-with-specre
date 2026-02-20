---
id: "01KHY7Q01EQ8V9ZJ5CZV72PA5F"
name: "collections_user_views_collections_system"
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
- spec/system/collections/user_views_collections_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Visiting` within the users domain.

### Behavioral Areas

- **Visiting collections**: shows all collections with articles

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: shows all collections with articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows all collections with articles

### S-2: does not show collections without articles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not show collections without articles

