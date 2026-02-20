---
id: "01KHY7Q1EW8TC20H18MD22ZJ4W"
name: "data_update_scripts_populate_suggested_tags_from_settings_lib"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/data_update_scripts_controller.rb
- spec/lib/data_update_scripts/populate_suggested_tags_from_settings_spec.rb

## Functional Overview

This specification defines the expected behavior of `Populate_Suggested_Tags_From_Settings` within the data_scripts domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/data_update_scripts_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: updates tags to use new boolean attribute (instead of settings)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates tags to use new boolean attribute (instead of settings)

