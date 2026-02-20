---
id: "01KHY7Q1211B44Q1NCWJRW8WEX"
name: "admin_nested_sidebar_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/nested_sidebar_spec.rb

## Functional Overview

This specification defines the expected behavior of `"admin` within the admin domain.

### Behavioral Areas

- **admin sidebar**: shows the option in the sidebar
- **sidebar menu options**: shows the option in the sidebar
- **tabbed menu options**: does not show the option in the tabbed header when the feature flag is disabled
- **profile admin feature flag**: does not show the option in the tabbed header when the feature flag is disabled
- **data update script admin feature flag**: does not show the option in the tabbed header when the feature flag is disabled


## Scenarios

### S-1: shows parent level and nested child items

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows parent level and nested child items

### S-2: shows nested grandchildren items where applicable

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows nested grandchildren items where applicable

### S-3: shows the option in the sidebar

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the option in the sidebar

### S-4: does not show the option in the tabbed header when the feature flag is disabled

- **Given** the system is in a standard operational state
- **When** the feature flag is disabled
- **Then** does not show the option in the tabbed header

### S-5: shows the option in the tabbed header when the feature flag is enabled

- **Given** the system is in a standard operational state
- **When** the feature flag is enabled
- **Then** shows the option in the tabbed header

