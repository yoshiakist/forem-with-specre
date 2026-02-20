---
id: "01KHY7Q03P8P8YQ89WRTWSJKD8"
name: "layouts_signup_modal.html.erb_view"
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
- spec/views/layouts/signup_modal.html.erb_spec.rb

## Functional Overview

This specification defines the expected behavior of `"layouts/_signup_modal"` within the users domain.

### Behavioral Areas

- **layouts/_signup_modal**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: renders the tagline if it is set

- **Given** it is set
- **When** the action is triggered
- **Then** renders the tagline

### S-2: does not render the tagline if it is not set

- **Given** it is not set
- **When** the action is triggered
- **Then** does not render the tagline

