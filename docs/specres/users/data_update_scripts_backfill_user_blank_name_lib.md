---
id: "01KHY7PZSNPA816S1VASA2MX9Z"
name: "data_update_scripts_backfill_user_blank_name_lib"
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
- spec/lib/data_update_scripts/backfill_user_blank_name_spec.rb

## Functional Overview

This specification defines the expected behavior of `Backfill_User_Blank_Name` within the users domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: replaces the blank name with the username

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** replaces the blank name with the username

### S-2: does not modify the name if it has trailing whitespaces

- **Given** it has trailing whitespaces
- **When** the action is triggered
- **Then** does not modify the name

### S-3: does not modify the name if it is valid

- **Given** it is valid
- **When** the action is triggered
- **Then** does not modify the name

