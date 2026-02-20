---
id: "01KHY7Q03EPVG78ADZN83YTQA9"
name: "user_views_a_reading_list_system"
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
- spec/system/user_views_a_reading_list_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Reading` within the users domain.

### Behavioral Areas

- **Reading list**: shows the large reading list
- **without tags**: Ensures correct behavior under the specified conditions
- **when large reading list**: shows the large reading list

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: shows the large reading list

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the large reading list

### S-2: /readinglist

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /readinglist

