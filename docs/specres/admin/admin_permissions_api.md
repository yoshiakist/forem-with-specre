---
id: "01KHY7Q12P8CK2NE15QYZY9S3S"
name: "admin_permissions_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/permissions_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/permissions"` within the admin domain.

### Behavioral Areas

- **/admin/permissions**: Ensures correct behavior under the specified conditions
- **when the user is not an admin**: Ensures correct behavior under the specified conditions
- **when the user is a super admin**: Ensures correct behavior under the specified conditions
- **when the user is a single resource admin**: Ensures correct behavior under the specified conditions
- **when the user is the wrong single resource admin**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: blocks the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** blocks the request

### S-2: allows the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows the request

### S-3: allows the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows the request

### S-4: blocks the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** blocks the request

