---
id: "01KHY7Q1406BWG5ZCSEXBE19XZ"
name: "admin_users_users_update_email_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/users/users_update_email_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/member_manager/users"` within the admin domain.

### Behavioral Areas

- **/admin/member_manager/users**: Ensures correct behavior under the specified conditions
- **PATCH /admin/member_manager/users/:id/update_email**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: updates the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the user

### S-2: creates a note that logs the old email and new email

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a note that logs the old email and new email

### S-3: redirects to the user admin page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to the user admin page

