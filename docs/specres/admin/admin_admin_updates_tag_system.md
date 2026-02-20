---
id: "01KHY7Q15C3H0297BQJP9ZB6BM"
name: "admin_admin_updates_tag_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/system/admin/admin_updates_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Admin` within the admin domain.

### Behavioral Areas

- **Admin updates a tag**: allows an Admin to successfully update a tag
- **when no colors have been chosen for the tag**: Ensures correct behavior under the specified conditions
- **when colors have already been chosen for the tag**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: allows an Admin to successfully update a tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows an Admin to successfully update a tag

### S-2: defaults to black and white upon update

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** defaults to black and white upon update

### S-3: remains the same color it was unless otherwise updated via the color picker

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** remains the same color it was unless otherwise updated via the color picker

