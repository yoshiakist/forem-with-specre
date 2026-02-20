---
id: "01KHY7Q0ZVBX1AE45MERS66WWR"
name: "admin_users_helper_helper"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/helpers/admin/users_helper_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users_Helper` within the admin domain.

### Behavioral Areas

- **role_options**: Ensures correct behavior under the specified conditions
- **format_last_activity_timestamp**: Ensures correct behavior under the specified conditions
- **cascading_high_level_roles**: Ensures correct behavior under the specified conditions
- **format_role_tooltip**: Ensures correct behavior under the specified conditions
- **user_status**: Ensures correct behavior under the specified conditions
- **overflow_count**: Ensures correct behavior under the specified conditions
- **organization_tooltip**: Ensures correct behavior under the specified conditions
- **when the limit is less than the total**: adds moderator role when feature flag enabled


## Scenarios

### S-1: returns base roles as statuses

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns base roles as statuses

### S-2: returns special roles as roles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns special roles as roles

### S-3: adds moderator role when feature flag enabled

- **Given** the system is in a standard operational state
- **When** feature flag enabled
- **Then** adds moderator role

### S-4: renders the proper 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper 

### S-5: renders the proper 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper 

### S-6: renders the proper 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper 

### S-7: renders the proper role for a Super Admin

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper role for a Super Admin

### S-8: renders the proper role for an Admin

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper role for an Admin

### S-9: renders the proper role for a Resource Admin

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper role for a Resource Admin

### S-10: renders the proper role for a user that isn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper role for a user that isn

### S-11: renders the proper tooltip for a Super Admin

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper tooltip for a Super Admin

### S-12: renders the proper tooltip for an Admin

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper tooltip for an Admin

