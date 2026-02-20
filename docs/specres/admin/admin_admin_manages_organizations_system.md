---
id: "01KHY7Q152E7D3TYNSNVX7VKE7"
name: "admin_admin_manages_organizations_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/system/admin/admin_manages_organizations_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Admin` within the admin domain.

### Behavioral Areas

- **Admin manages organizations**: searches for organizations
- **when searching for organizations**: searches for organizations
- **when managing credits for a single organization**: searches for organizations


## Scenarios

### S-1: searches for organizations

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** searches for organizations

### S-2: does not show the remove form when there are no credits

- **Given** the system is in a standard operational state
- **When** there are no credits
- **Then** does not show the remove form

