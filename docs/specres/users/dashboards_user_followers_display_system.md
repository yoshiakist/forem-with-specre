---
id: "01KHY7Q01GHFZNNEA50F7VVNP3"
name: "dashboards_user_followers_display_system"
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
- spec/system/dashboards/user_followers_display_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Followers` within the users domain.

### Behavioral Areas

- **Followers Dashboard**: /dashboard/user_followers
- **when /dashboard/user_followers is visited**: /dashboard/user_followers

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: displays correct following buttons

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays correct following buttons

### S-2: /dashboard/user_followers

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /dashboard/user_followers

