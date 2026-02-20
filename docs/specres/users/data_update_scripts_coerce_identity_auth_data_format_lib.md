---
id: "01KHY7PZSQHCK7HWA6ZC3KBA8N"
name: "data_update_scripts_coerce_identity_auth_data_format_lib"
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
- spec/lib/data_update_scripts/coerce_identity_auth_data_format_spec.rb

## Functional Overview

This specification defines the expected behavior of `Coerce_Identity_Auth_Data_Format` within the users domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: changes hash auth data dumps to AuthHash

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** changes hash auth data dumps to AuthHash

### S-2: handles null values safely

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles null values safely

