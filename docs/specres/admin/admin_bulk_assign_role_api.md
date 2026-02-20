---
id: "01KHY7Q10NJ10KG9D5WSD9N8QW"
name: "admin_bulk_assign_role_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/bulk_assign_role_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Admin::BulkAssignRole"` within the admin domain.

### Behavioral Areas

- **Admin::BulkAssignRole**: Ensures correct behavior under the specified conditions
- **POST /admin/member_manager/bulk_assign_role**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: adds trusted role successfully

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds trusted role successfully

### S-2: adds role with extra whitespace in usernames

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds role with extra whitespace in usernames

### S-3: shows error if role is blank

- **Given** role is blank
- **When** the action is triggered
- **Then** shows error

### S-4: adds default note if user input is empty

- **Given** user input is empty
- **When** the action is triggered
- **Then** adds default note

### S-5: adds role to valid usernames only and creates user_not_found AuditLog

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds role to valid usernames only and creates user_not_found AuditLog

### S-6: adds successful AuditLog

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds successful AuditLog

### S-7: adds role already applied AuditLog

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds role already applied AuditLog

