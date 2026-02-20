---
id: "01KHY7Q10GKT211246BX1Y4GW2"
name: "admin_billboards_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/billboards_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/customization/billboards"` within the admin domain.

### Behavioral Areas

- **/admin/customization/billboards**: Ensures correct behavior under the specified conditions
- **when the user is not an admin**: sets creator to current_user
- **GET /admin/customization/billboards**: Ensures correct behavior under the specified conditions
- **POST /admin/customization/billboards**: Ensures correct behavior under the specified conditions
- **when the user is a super admin**: sets creator to current_user
- **GET /admin/customization/billboards**: Ensures correct behavior under the specified conditions
- **GET /admin/customization/billboards/:id/edit**: Ensures correct behavior under the specified conditions
- **GET /admin/customization/billboards/:id**: Ensures correct behavior under the specified conditions


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

### S-4: allows the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows the request

### S-5: allows the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows the request

### S-6: creates a new billboard

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new billboard

### S-7: sets creator to current_user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets creator to current_user

### S-8: fails to create a new billboard with invalid target geolocations

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** fails to create a new billboard with invalid target geolocations

### S-9: creates a new billboard with no target geolocations

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new billboard with no target geolocations

### S-10: updates Billboard

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates Billboard

### S-11: updates Billboard

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates Billboard

### S-12: redirects back to edit path

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects back to edit path

