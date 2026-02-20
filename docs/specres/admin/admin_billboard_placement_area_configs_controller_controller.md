---
id: "01KHY7Q0ZKZHN5NVVXW9JH1ZTJ"
name: "admin_billboard_placement_area_configs_controller_controller"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/controllers/admin/billboard_placement_area_configs_controller_spec.rb

## Functional Overview

This specification defines the expected behavior of `Admin::BillboardPlacementAreaConfigsController` within the admin domain.

### Behavioral Areas

- **GET #index**: Ensures correct behavior under the specified conditions
- **GET #edit**: Ensures correct behavior under the specified conditions
- **PATCH #update**: Ensures correct behavior under the specified conditions
- **with valid params**: redirects to index with success message
- **with invalid params**: redirects to index with success message
- **with edge case params**: redirects to index with success message


## Scenarios

### S-1: returns http success

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns http success

### S-2: loads all configs ordered by placement_area

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** loads all configs ordered by placement_area

### S-3: creates missing configs for all placement areas

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates missing configs for all placement areas

### S-4: handles errors when creating missing configs gracefully

- **Given** the system is in a standard operational state
- **When** creating missing configs gracefully
- **Then** handles errors

### S-5: returns http success

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns http success

### S-6: loads the config

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** loads the config

### S-7: sets the human readable area name

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the human readable area name

### S-8: updates the config

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the config

### S-9: redirects to index with success message

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to index with success message

### S-10: does not update the config

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not update the config

### S-11: renders edit template with error message

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders edit template with error message

### S-12: sanitizes negative weight values to 0

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sanitizes negative weight values to 0

