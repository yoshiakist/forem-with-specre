---
id: "01KHY7Q10KD8D0DH11B06PYX6B"
name: "admin_broadcasts_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/broadcasts_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/advanced/broadcasts"` within the admin domain.

### Behavioral Areas

- **/admin/advanced/broadcasts**: Ensures correct behavior under the specified conditions
- **when the user is not an admin**: Ensures correct behavior under the specified conditions
- **GET /admin/advanced/broadcasts**: Ensures correct behavior under the specified conditions
- **POST /admin/advanced/broadcasts**: Ensures correct behavior under the specified conditions
- **when the user is a super admin**: Ensures correct behavior under the specified conditions
- **GET /admin/advanced/broadcasts**: Ensures correct behavior under the specified conditions
- **POST /admin/advanced/broadcasts**: Ensures correct behavior under the specified conditions
- **PUT /admin/advanced/broadcasts**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: blocks the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** blocks the request

### S-2: blocks the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** blocks the request

### S-3: allows the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows the request

### S-4: creates a new broadcast

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new broadcast

### S-5: updates the Broadcast

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the Broadcast

### S-6: deletes the broadcast

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes the broadcast

### S-7: allows the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows the request

### S-8: creates a new broadcast

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new broadcast

### S-9: deletes the broadcast

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes the broadcast

### S-10: blocks the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** blocks the request

### S-11: blocks the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** blocks the request

### S-12: does not allow a second broadcast to be set to active

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow a second broadcast to be set to active

