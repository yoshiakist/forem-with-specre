---
id: "01KHY7Q1295FHBEGB1FJRPT69E"
name: "admin_organizations_fully_trusted_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/organizations_fully_trusted_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/content_manager/organizations` within the admin domain.

### Behavioral Areas

- **/admin/content_manager/organizations fully_trusted**: enables fully_trusted status
- **PATCH /admin/organizations/:id/update_fully_trusted**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: enables fully_trusted status

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enables fully_trusted status

### S-2: disables fully_trusted status

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** disables fully_trusted status

### S-3: creates a note when updating

- **Given** the system is in a standard operational state
- **When** updating
- **Then** creates a note

