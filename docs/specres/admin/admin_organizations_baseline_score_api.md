---
id: "01KHY7Q126GSGP88HTM2KX4K7M"
name: "admin_organizations_baseline_score_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/organizations_baseline_score_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Update` within the admin domain.

### Behavioral Areas

- **Update Organization Baseline Score**: updates the baseline_score successfully
- **PATCH /admin/content_manager/organizations/:id/update_baseline_score**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: updates the baseline_score successfully

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the baseline_score successfully

### S-2: creates an audit note for the change

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an audit note for the change

### S-3: works when updating from a non-zero value

- **Given** the system is in a standard operational state
- **When** updating from a non-zero value
- **Then** works

### S-4: raises an error for negative values

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises an error for negative values

