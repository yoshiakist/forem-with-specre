---
id: "01KHY7Q11385RHRQX0N8ZVS8Y9"
name: "admin_data_update_scripts_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/data_update_scripts_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/advanced/data_update_scripts"` within the admin domain.

### Behavioral Areas

- **/admin/advanced/data_update_scripts**: Ensures correct behavior under the specified conditions
- **when the user is not an tech admin**: Ensures correct behavior under the specified conditions
- **GET /admin/advanced/data_update_scripts**: Ensures correct behavior under the specified conditions
- **when the user is a tech admin**: Ensures correct behavior under the specified conditions
- **GET /admin/advanced/data_update_scripts**: Ensures correct behavior under the specified conditions
- **GET /admin/advanced/data_update_scripts/:id**: Ensures correct behavior under the specified conditions
- **POST /admin/:id/force_run**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: blocks the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** blocks the request

### S-2: allows the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows the request

### S-3: displays the data_update_scripts

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays the data_update_scripts

### S-4: displays a 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays a 

### S-5: returns a data update script

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a data update script

### S-6: calls the the sidekiq worker

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls the the sidekiq worker

