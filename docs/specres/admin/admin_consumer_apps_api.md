---
id: "01KHY7Q10YH8SST7GNXF40ZHA2"
name: "admin_consumer_apps_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/consumer_apps_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Admin` within the admin domain.

### Behavioral Areas

- **Admin - Consumer Apps**: creates a new consumer_app
- **when the user is not an admin**: fails when trying to create duplicate apps (app_bundle + platform)
- **GET /admin/consumer_apps**: Ensures correct behavior under the specified conditions
- **POST /admin/consumer_apps**: Ensures correct behavior under the specified conditions
- **when the user is a super admin**: fails when trying to create duplicate apps (app_bundle + platform)
- **GET /admin/consumer_apps**: Ensures correct behavior under the specified conditions
- **POST /admin/consumer_apps**: Ensures correct behavior under the specified conditions
- **PUT /admin/consumer_apps**: Ensures correct behavior under the specified conditions


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

### S-4: creates a new consumer_app

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new consumer_app

### S-5: updates the ConsumerApp

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the ConsumerApp

### S-6: deletes the ConsumerApp

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes the ConsumerApp

### S-7: allows the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows the request

### S-8: creates a new ConsumerApp

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new ConsumerApp

### S-9: fails when trying to create duplicate apps (app_bundle + platform)

- **Given** the system is in a standard operational state
- **When** trying to create duplicate apps (app_bundle + platform)
- **Then** fails

### S-10: updates the ConsumerApp

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the ConsumerApp

### S-11: deletes the ConsumerApp

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes the ConsumerApp

### S-12: blocks the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** blocks the request

