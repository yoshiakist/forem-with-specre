---
id: "01KHY7Q14N8GAYBPQ5X9675SPD"
name: "admin_admin_awards_badges_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/system/admin/admin_awards_badges_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Admin` within the admin domain.

### Behavioral Areas

- **Admin awards badges**: lists the badges


## Scenarios

### S-1: loads the view

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** loads the view

### S-2: lists the badges

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** lists the badges

### S-3: awards badges

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** awards badges

### S-4: /#{user.username}/

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{user.username}/

### S-5: does not award badges if no badge is selected

- **Given** no badge is selected
- **When** the action is triggered
- **Then** does not award badges

