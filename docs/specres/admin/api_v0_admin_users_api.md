---
id: "01KHY7Q14BH4VTGJ2ZV0EDW9DJ"
name: "api_v0_admin_users_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/api/v0/admin/users_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/api/admin/users"` within the admin domain.

### Behavioral Areas

- **/api/admin/users**: Ensures correct behavior under the specified conditions
- **when unauthorized**: Ensures correct behavior under the specified conditions
- **when authorized**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: rejects requests without an authorization token

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects requests without an authorization token

### S-2: rejects requests with a non-admin token

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects requests with a non-admin token

### S-3: rejects requests with a regular admin token

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects requests with a regular admin token

### S-4: accepts reqeuest with a super-admin token

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts reqeuest with a super-admin token

