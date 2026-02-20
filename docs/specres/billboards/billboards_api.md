---
id: "01KHY7Q0XNPJ1FG3967EQPTA42"
name: "billboards_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/billboards_controller.rb
- app/controllers/api/v1/billboards_controller.rb
- app/controllers/billboards_controller.rb
- spec/requests/billboards_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Billboards"` within the billboards domain.

### Behavioral Areas

- **Billboards**: includes billboards that target user
- **GET /:username/:slug/billboards/:placement_area with role-based filtering**: uses default cache expiry for placement areas without config
- **when target_role_names includes user**: includes billboards that target user
- **when exclude_role_names includes user**: includes billboards that target user
- **when target_role_names does not include user**: includes billboards that target user
- **when exclude_role_names does not include user**: includes billboards that target user
- **when both target_role_names and exclude_role_names are empty**: returns an empty style string
- **GET /:username/:slug/billboards/:color**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/billboards_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/billboards_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/billboards_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: includes billboards that target user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes billboards that target user

### S-2: excludes billboards that should not be shown to user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** excludes billboards that should not be shown to user

### S-3: excludes billboards that do not target user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** excludes billboards that do not target user

### S-4: includes billboards that are not excluded for user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes billboards that are not excluded for user

### S-5: includes billboards that have no role restrictions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes billboards that have no role restrictions

### S-6: includes the correct style string

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes the correct style string

### S-7: includes the correct style string

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes the correct style string

### S-8: returns an empty style string

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an empty style string

### S-9: returns the correct response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct response

### S-10: returns only billboards targeting their location

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns only billboards targeting their location

### S-11: is accurate for more precise locations

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is accurate for more precise locations

### S-12: does not set Vary header

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not set Vary header

