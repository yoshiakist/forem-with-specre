---
id: "01KHY7Q11004H3J2ZQC4506B0Y"
name: "admin_creator_settings_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/creator_settings_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/creator_settings/new"` within the admin domain.

### Behavioral Areas

- **/creator_settings/new**: Ensures correct behavior under the specified conditions
- **GET /admin/creator_settings/new**: Ensures correct behavior under the specified conditions
- **when the user is a creator**: allows a creator to successfully fill out the creator setup form
- **when the user is a not a creator**: allows a creator to successfully fill out the creator setup form
- **POST /admin/creator_settings/new**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: allows the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows the request

### S-2: renders the correct page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the correct page

### S-3: blocks the request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** blocks the request

### S-4: allows a creator to successfully fill out the creator setup form

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows a creator to successfully fill out the creator setup form

### S-5: updates settings admin action taken

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates settings admin action taken

