---
id: "01KHY7Q13S2WPV7XAKF517A7DF"
name: "admin_users_users_change_max_score_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/users/users_change_max_score_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/member_manager/users"` within the admin domain.

### Behavioral Areas

- **/admin/member_manager/users**: Ensures correct behavior under the specified conditions
- **PATCH /admin/member_manager/users/:id/max_score**: Ensures correct behavior under the specified conditions
- **when the update fails**: updates the user


## Scenarios

### S-1: updates the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the user

### S-2: creates a note with the reason for the change

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a note with the reason for the change

### S-3: redirects to the user admin page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to the user admin page

### S-4: sets a flash error message

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets a flash error message

