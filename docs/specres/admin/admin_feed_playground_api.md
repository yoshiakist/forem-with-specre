---
id: "01KHY7Q11A4CW0Z6TBVYXEB2E6"
name: "admin_feed_playground_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/feed_playground_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/advanced/tools/feed_playground"` within the admin domain.

### Behavioral Areas

- **/admin/advanced/tools/feed_playground**: Ensures correct behavior under the specified conditions
- **GET /admin/advanced/tools/feed_playground**: Ensures correct behavior under the specified conditions
- **when the user is not an admin**: Ensures correct behavior under the specified conditions
- **when the user is a super admin**: Ensures correct behavior under the specified conditions
- **when the user is a single resource admin**: Ensures correct behavior under the specified conditions
- **when the user is the wrong single resource admin**: Ensures correct behavior under the specified conditions
- **POST /admin/advanced/tools/feed_playground**: Ensures correct behavior under the specified conditions
- **when the user is a super admin**: Ensures correct behavior under the specified conditions


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

### S-5: allows the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows the request

### S-6: shows proper error

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows proper error

