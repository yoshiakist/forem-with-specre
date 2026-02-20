---
id: "01KHY7Q12XWCNJ7VCH1F6N1MVB"
name: "admin_profile_field_groups_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/profile_field_groups_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/customization/profile_field_groups"` within the admin domain.

### Behavioral Areas

- **/admin/customization/profile_field_groups**: Ensures correct behavior under the specified conditions
- **POST /admin/customization/profile_field_groups**: Ensures correct behavior under the specified conditions
- **PUT /admin/customization/profile_field_groups/:id**: Ensures correct behavior under the specified conditions
- **DELETE /admin/profile_fields/:id**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: redirects successfully

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects successfully

### S-2: creates a profile_field_group

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a profile_field_group

### S-3: redirects successfully

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects successfully

### S-4: updates the profile field values

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the profile field values

### S-5: redirects successfully

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects successfully

### S-6: removes a profile_field_group

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes a profile_field_group

