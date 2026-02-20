---
id: "01KHY7Q12V641EKE7Z711V1X4F"
name: "admin_privileged_reactions_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/privileged_reactions_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/moderations/privileged_reactions"` within the admin domain.

### Behavioral Areas

- **/admin/moderations/privileged_reactions**: Ensures correct behavior under the specified conditions
- **when the user is not an admin**: Ensures correct behavior under the specified conditions
- **when the user is a single resource admin**: Ensures correct behavior under the specified conditions
- **when the user is an admin**: Ensures correct behavior under the specified conditions
- **GETS /admin/moderations/privileged_reactions**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: blocks the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** blocks the request

### S-2: renders with status 200

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders with status 200

### S-3: does not block the request

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not block the request

### S-4: renders to appropriate page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders to appropriate page

