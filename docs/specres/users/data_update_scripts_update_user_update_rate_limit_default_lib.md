---
id: "01KHY7PZSWN97RNGF4MFV532PH"
name: "data_update_scripts_update_user_update_rate_limit_default_lib"
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
- spec/lib/data_update_scripts/update_user_update_rate_limit_default_spec.rb

## Functional Overview

This specification defines the expected behavior of `Update_User_Update_Rate_Limit_Default` within the users domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: updates rate limit if 5 or less

- **Given** 5 or less
- **When** the action is triggered
- **Then** updates rate limit

### S-2: does NOT update the rate limit if greater than 5

- **Given** greater than 5
- **When** the action is triggered
- **Then** does NOT update the rate limit

