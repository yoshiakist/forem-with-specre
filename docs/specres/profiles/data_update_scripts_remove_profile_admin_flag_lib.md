---
id: "01KHY7Q0K48JPKDXDVZRCPX2ED"
name: "data_update_scripts_remove_profile_admin_flag_lib"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/profile_field_groups_controller.rb
- app/controllers/admin/profile_fields_controller.rb
- app/controllers/api/v0/profile_images_controller.rb
- app/controllers/api/v1/profile_images_controller.rb
- app/controllers/concerns/api/profile_images_controller.rb
- app/controllers/profile_field_groups_controller.rb
- spec/lib/data_update_scripts/remove_profile_admin_flag_spec.rb

## Functional Overview

This specification defines the expected behavior of `Remove_Profile_Admin_Flag` within the profiles domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/profile_field_groups_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/profile_fields_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/profile_field_groups_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: causes enabled? to be false

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** causes enabled? to be false

### S-2: removes the profile_admin flag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes the profile_admin flag

### S-3: works if the flag does not exist

- **Given** the flag does not exist
- **When** the action is triggered
- **Then** works

