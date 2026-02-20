---
id: "01KHY7Q13CTARYM9F87K21A5Z5"
name: "admin_subforems_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/subforems_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Admin::Subforems"` within the admin domain.

### Behavioral Areas

- **Admin::Subforems**: Ensures correct behavior under the specified conditions
- **GET /admin/subforems**: Ensures correct behavior under the specified conditions
- **GET /admin/subforems/new**: Ensures correct behavior under the specified conditions
- **POST /admin/subforems**: Ensures correct behavior under the specified conditions
- **with create_from_scratch parameters**: creates a new subforem using create_from_scratch! and queues background job
- **with regular parameters (fallback)**: works without background image URL
- **with invalid parameters**: works without background image URL
- **with partial create_from_scratch parameters**: creates a new subforem using create_from_scratch! and queues background job


## Scenarios

### S-1: returns a successful response and lists subforems

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a successful response and lists subforems

### S-2: renders the new subforem form

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the new subforem form

### S-3: includes all the new form fields

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes all the new form fields

### S-4: creates a new subforem using create_from_scratch! and queues background job

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new subforem using create_from_scratch! and queues background job

### S-5: works without background image URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** works without background image URL

### S-6: creates a new subforem using regular save and redirects to the index

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new subforem using regular save and redirects to the index

### S-7: does not create a subforem and re-renders the new form with errors

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create a subforem and re-renders the new form with errors

### S-8: falls back to regular creation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** falls back to regular creation

### S-9: renders the edit form

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the edit form

### S-10: updates the subforem and redirects to the index

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the subforem and redirects to the index

