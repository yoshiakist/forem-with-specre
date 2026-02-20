---
id: "01KHY7Q0V80JA0PB9TD8NF44T8"
name: "data_update_scripts_backfill_navigation_links_column_display_to_lib"
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
- spec/lib/data_update_scripts/backfill_navigation_links_column_display_to_spec.rb

## Functional Overview

This specification defines the expected behavior of `Backfill_Navigation_Links_Column_Display_To` within the pages domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/navigation_links_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/page_templates_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/pages_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/pages_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/pages_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/navigation_link.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: backfills relevant navigation links with 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** backfills relevant navigation links with 

### S-2: leaves visible-to-all navigation links unchanged

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** leaves visible-to-all navigation links unchanged

