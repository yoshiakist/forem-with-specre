---
id: "01KHY7Q12RK9MCVEHN73ER6146"
name: "admin_podcasts_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/podcasts_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/content_manager/podcasts"` within the admin domain.

### Behavioral Areas

- **/admin/content_manager/podcasts**: Ensures correct behavior under the specified conditions
- **GET /admin/content_manager/podcasts**: Ensures correct behavior under the specified conditions
- **Adding owner**: adds an owner
- **Updating**: Ensures correct behavior under the specified conditions
- **POST /admin/content_manager/podcasts/:id/fetch_podcasts**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: renders success

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders success

### S-2: displays podcasts with and without episodes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays podcasts with and without episodes

### S-3: adds an owner

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds an owner

### S-4: does nothing when adding a non-existent user as owner

- **Given** the system is in a standard operational state
- **When** adding a non-existent user as owner
- **Then** does nothing

### S-5: updates the podcast

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the podcast

### S-6: updates image & pattern_image

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates image & pattern_image

### S-7: redirects after update

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects after update

### S-8: redirects back to index with a notice

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects back to index with a notice

### S-9: schedules a worker to fetch episodes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** schedules a worker to fetch episodes

### S-10: schedules a worker without limit and with force

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** schedules a worker without limit and with force

