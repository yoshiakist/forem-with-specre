---
id: "01KHY7Q0VFTGK1FGTDZ9PGM3WV"
name: "data_update_scripts_make_local_navigation_links_relative_lib"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/navigation_links_controller.rb
- app/controllers/admin/page_templates_controller.rb
- app/controllers/admin/pages_controller.rb
- app/controllers/api/v1/pages_controller.rb
- app/controllers/pages_controller.rb
- app/models/navigation_link.rb
- spec/lib/data_update_scripts/make_local_navigation_links_relative_spec.rb

## Functional Overview

This specification defines the expected behavior of `Make_Local_Navigation_Links_Relative` within the pages domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/navigation_links_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/page_templates_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/pages_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/pages_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/pages_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/navigation_link.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: makes local navigation links relative

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** makes local navigation links relative

### S-2: leaves external navigation links unchanged

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** leaves external navigation links unchanged

