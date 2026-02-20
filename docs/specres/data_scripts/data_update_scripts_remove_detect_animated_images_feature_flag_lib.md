---
id: "01KHY7Q1F61YW6V9YWKZRKP2RJ"
name: "data_update_scripts_remove_detect_animated_images_feature_flag_lib"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/data_update_scripts_controller.rb
- spec/lib/data_update_scripts/remove_detect_animated_images_feature_flag_spec.rb

## Functional Overview

This specification defines the expected behavior of `Remove_Detect_Animated_Images_Feature_Flag` within the data_scripts domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/data_update_scripts_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: removes the :detect_animated_images flag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes the :detect_animated_images flag

### S-2: works if the flag is not available

- **Given** the flag is not available
- **When** the action is triggered
- **Then** works

