---
id: "01KHY7Q14E7WVQAWF9J3T93JFK"
name: "api_v1_admin_users_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/api/v1/admin/users_spec.rb

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

### S-4: accepts request with a super-admin token

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts request with a super-admin token

### S-5: enqueues an invitation email to be sent with custom options

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enqueues an invitation email to be sent with custom options

### S-6: marks user as registered false

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** marks user as registered false

