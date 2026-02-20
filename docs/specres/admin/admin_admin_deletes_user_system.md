---
id: "01KHY7Q14XCDQ6MA6K5NZJ6KP0"
name: "admin_admin_deletes_user_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/system/admin/admin_deletes_user_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Admin` within the admin domain.

### Behavioral Areas

- **Admin deletes user**: enqueues a job for deleting the user


## Scenarios

### S-1: enqueues a job for deleting the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enqueues a job for deleting the user

### S-2: deletes users when they have no email address

- **Given** the system is in a standard operational state
- **When** they have no email address
- **Then** deletes users

