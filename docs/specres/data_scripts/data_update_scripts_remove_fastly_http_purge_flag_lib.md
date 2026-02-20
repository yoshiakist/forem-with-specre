---
id: "01KHY7Q1F8EZN3TGDW91N8TYV3"
name: "data_update_scripts_remove_fastly_http_purge_flag_lib"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/data_update_scripts_controller.rb
- spec/lib/data_update_scripts/remove_fastly_http_purge_flag_spec.rb

## Functional Overview

This specification defines the expected behavior of `Remove_Fastly_Http_Purge_Flag` within the data_scripts domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/data_update_scripts_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: removes the feature flag if present

- **Given** present
- **When** the action is triggered
- **Then** removes the feature flag

### S-2: is safe to run twice

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is safe to run twice

