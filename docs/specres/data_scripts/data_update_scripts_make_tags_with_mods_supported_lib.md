---
id: "01KHY7Q1EG4CK9GTCF3Z5AXR3D"
name: "data_update_scripts_make_tags_with_mods_supported_lib"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/data_update_scripts_controller.rb
- spec/lib/data_update_scripts/make_tags_with_mods_supported_spec.rb

## Functional Overview

This specification defines the expected behavior of `Make_Tags_With_Mods_Supported` within the data_scripts domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/data_update_scripts_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: sets tags with moderators to supported

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets tags with moderators to supported

