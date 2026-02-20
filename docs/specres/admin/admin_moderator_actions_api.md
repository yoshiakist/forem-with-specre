---
id: "01KHY7Q11QVSHRA2025SNVJKBF"
name: "admin_moderator_actions_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/moderator_actions_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/moderation/moderator_reactions"` within the admin domain.

### Behavioral Areas

- **/admin/moderation/moderator_reactions**: Ensures correct behavior under the specified conditions
- **when the user is not an admin**: renders the page with a user
- **when the user is a single resource admin**: renders the page with a user
- **when the user is an admin**: renders the page with a user


## Scenarios

### S-1: blocks the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** blocks the request

### S-2: renders the page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the page

### S-3: does not block the request

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not block the request

### S-4: renders the page with a user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the page with a user

### S-5: renders the page with an audit log not belonging to a specific user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the page with an audit log not belonging to a specific user

