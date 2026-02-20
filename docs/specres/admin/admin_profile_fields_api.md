---
id: "01KHY7Q130PE2BJBJPA3YTXXEV"
name: "admin_profile_fields_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/profile_fields_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/customization/profile_fields"` within the admin domain.

### Behavioral Areas

- **/admin/customization/profile_fields**: Ensures correct behavior under the specified conditions
- **GET /admin/customization/profile_fields**: Ensures correct behavior under the specified conditions
- **POST /admin/customization/profile_fields**: Ensures correct behavior under the specified conditions
- **PUT /admin/profile_fields/:id**: Ensures correct behavior under the specified conditions
- **DELETE /admin/profile_fields/:id**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: renders successfully

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders successfully

### S-2: lists the profile fields

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** lists the profile fields

### S-3: redirects successfully

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects successfully

### S-4: creates a profile_field

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a profile_field

### S-5: redirects successfully

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects successfully

### S-6: updates the profile field values

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the profile field values

### S-7: redirects successfully

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects successfully

### S-8: removes a profile field

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes a profile field

