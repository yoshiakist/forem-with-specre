---
id: "01KHY7Q12B2R9DPMZGXASAVN4C"
name: "admin_organizations_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/organizations_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/content_manager/organizations"` within the admin domain.

### Behavioral Areas

- **/admin/content_manager/organizations**: Ensures correct behavior under the specified conditions
- **GETS /admin/content_manager/organizations**: Ensures correct behavior under the specified conditions
- **GET /admin/organizations/:id**: Ensures correct behavior under the specified conditions
- **PATCH /admin**: Ensures correct behavior under the specified conditions
- **PATCH /admin/organizations/:id/update_fully_trusted**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: lists all organizations

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** lists all organizations

### S-2: allows searching

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows searching

### S-3: renders the correct organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the correct organization

### S-4: adds credits to an organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds credits to an organization

### S-5: removes credits to an organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes credits to an organization

### S-6: enables fully_trusted status

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enables fully_trusted status

### S-7: disables fully_trusted status

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** disables fully_trusted status

