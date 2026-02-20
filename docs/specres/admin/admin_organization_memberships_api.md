---
id: "01KHY7Q1245KCH2Q3VQBF4Q7KT"
name: "admin_organization_memberships_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/organization_memberships_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/organization_memberships"` within the admin domain.

### Behavioral Areas

- **/admin/organization_memberships**: Ensures correct behavior under the specified conditions
- **create**: Ensures correct behavior under the specified conditions
- **when interacting via a browser**: Ensures correct behavior under the specified conditions
- **when interacting via ajax**: Ensures correct behavior under the specified conditions
- **update**: Ensures correct behavior under the specified conditions
- **when interacting via a browser**: Ensures correct behavior under the specified conditions
- **when interacting via ajax**: Ensures correct behavior under the specified conditions
- **destroy**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: errors if a param is missing

- **Given** a param is missing
- **When** the action is triggered
- **Then** errors

### S-2: errors if a param is invalid

- **Given** a param is invalid
- **When** the action is triggered
- **Then** errors

### S-3: adds a user to an organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds a user to an organization

### S-4: returns :unprocessable_entity if a param is missing

- **Given** a param is missing
- **When** the action is triggered
- **Then** returns :unprocessable_entity

### S-5: returns :unprocessable_entity if a param is invalid

- **Given** a param is invalid
- **When** the action is triggered
- **Then** returns :unprocessable_entity

### S-6: adds a user to an organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds a user to an organization

### S-7: returns not found for non existing memberships

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns not found for non existing memberships

### S-8: errors if a param is invalid

- **Given** a param is invalid
- **When** the action is triggered
- **Then** errors

### S-9: cannot change the user id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** cannot change the user id

### S-10: cannot change the organization id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** cannot change the organization id

### S-11: changes the membership type of user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** changes the membership type of user

### S-12: errors if a param is invalid

- **Given** a param is invalid
- **When** the action is triggered
- **Then** errors

