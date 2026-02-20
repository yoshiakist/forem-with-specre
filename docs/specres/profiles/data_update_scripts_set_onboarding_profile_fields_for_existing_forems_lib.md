---
id: "01KHY7Q0K9WVVDQ1YMTF03NJ0A"
name: "data_update_scripts_set_onboarding_profile_fields_for_existing_forems_lib"
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
- spec/lib/data_update_scripts/set_onboarding_profile_fields_for_existing_forems_spec.rb

## Functional Overview

This specification defines the expected behavior of `Set_Onboarding_Profile_Fields_For_Existing_Forems` within the profiles domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/profile_field_groups_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/profile_fields_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/profile_images_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/profile_field_groups_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: toggles show_in_onboarding to true for specific profile fields

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** toggles show_in_onboarding to true for specific profile fields

### S-2: updates the labels for specific profile fields

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the labels for specific profile fields

