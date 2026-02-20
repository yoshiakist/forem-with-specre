---
id: "01KHY7Q1DQN49G6KFYVQ8VHN7A"
name: "data_update_scripts_add_fastly_http_purge_feature_flag_lib"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/data_update_scripts_controller.rb
- spec/lib/data_update_scripts/add_fastly_http_purge_feature_flag_spec.rb

## Functional Overview

This specification defines the expected behavior of `Add_Fastly_Http_Purge_Feature_Flag` within the data_scripts domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/data_update_scripts_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: adds the :fastly_http_purge flag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds the :fastly_http_purge flag

### S-2: works if the flag is already available

- **Given** the flag is already available
- **When** the action is triggered
- **Then** works

