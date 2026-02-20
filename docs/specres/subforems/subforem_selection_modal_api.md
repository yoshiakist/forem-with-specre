---
id: "01KHY7Q1BH5PWX6C9D0A0YXF58"
name: "subforem_selection_modal_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/subforem_moderators/moderators_controller.rb
- app/controllers/admin/subforems_controller.rb
- app/controllers/api/v0/subforems_controller.rb
- app/controllers/api/v1/subforems_controller.rb
- app/controllers/concerns/api/subforems_controller.rb
- app/controllers/subforems_controller.rb
- spec/requests/subforem_selection_modal_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Subforem` within the subforems domain.

### Behavioral Areas

- **Subforem Selection Modal**: includes the subforem selection modal when on root subforem
- **Modal presence in layout**: includes the subforem selection modal when on root subforem

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/subforem_moderators/moderators_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/subforems_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/subforems_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/subforems_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/subforems_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/subforems_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: includes the subforem selection modal when on root subforem

- **Given** the system is in a standard operational state
- **When** on root subforem
- **Then** includes the subforem selection modal

### S-2: does not include the modal when not on root subforem

- **Given** the system is in a standard operational state
- **When** not on root subforem
- **Then** does not include the modal

