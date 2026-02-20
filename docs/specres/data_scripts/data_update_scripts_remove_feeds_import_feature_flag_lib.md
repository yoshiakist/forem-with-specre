---
id: "01KHY7Q1FBM0RVY9QJSE6W6W34"
name: "data_update_scripts_remove_feeds_import_feature_flag_lib"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/data_update_scripts_controller.rb
- spec/lib/data_update_scripts/remove_feeds_import_feature_flag_spec.rb

## Functional Overview

This specification defines the expected behavior of `Remove_Feeds_Import_Feature_Flag` within the data_scripts domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/data_update_scripts_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: removes the :feeds_import flag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes the :feeds_import flag

### S-2: works if the flag is not available

- **Given** the flag is not available
- **When** the action is triggered
- **Then** works

