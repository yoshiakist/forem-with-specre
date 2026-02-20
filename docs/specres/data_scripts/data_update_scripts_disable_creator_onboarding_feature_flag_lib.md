---
id: "01KHY7Q1E8DE95AGZHA1RMT8E3"
name: "data_update_scripts_disable_creator_onboarding_feature_flag_lib"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/data_update_scripts_controller.rb
- spec/lib/data_update_scripts/disable_creator_onboarding_feature_flag_spec.rb

## Functional Overview

This specification defines the expected behavior of `Disable_Creator_Onboarding_Feature_Flag` within the data_scripts domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/data_update_scripts_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: disables the :creator_onboarding feature flag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** disables the :creator_onboarding feature flag

### S-2: works if not already enabled

- **Given** not already enabled
- **When** the action is triggered
- **Then** works

