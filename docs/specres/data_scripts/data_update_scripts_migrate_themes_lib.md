---
id: "01KHY7Q1EJSYNJQ73TW9V52VSG"
name: "data_update_scripts_migrate_themes_lib"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/data_update_scripts_controller.rb
- spec/lib/data_update_scripts/migrate_themes_spec.rb

## Functional Overview

This specification defines the expected behavior of `Migrate_Themes` within the data_scripts domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/data_update_scripts_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: leaves default theme users on light and leaves OS sync enabled

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** leaves default theme users on light and leaves OS sync enabled

### S-2: updates minimal theme users to light and disables OS sync

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates minimal theme users to light and disables OS sync

### S-3: updates night theme users to dark and disables OS sync

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates night theme users to dark and disables OS sync

### S-4: updates pink theme users to light and leaves OS sync enabled

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates pink theme users to light and leaves OS sync enabled

### S-5: updates ten x hacker theme users to dark and disables OS sync

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates ten x hacker theme users to dark and disables OS sync

