---
id: "01KHY7Q1359DT2EHA9FPG2BR3E"
name: "admin_response_templates_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/response_templates_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/advanced/response_templates"` within the admin domain.

### Behavioral Areas

- **/admin/advanced/response_templates**: Ensures correct behavior under the specified conditions
- **GET /admin/advanced/response_templates**: Ensures correct behavior under the specified conditions
- **when there are response templates to render**: renders with status 200
- **when a single resource admin**: Ensures correct behavior under the specified conditions
- **GET /admin/advanced/response_templates/new**: Ensures correct behavior under the specified conditions
- **POST /admin/advanced/response_templates**: Ensures correct behavior under the specified conditions
- **GET /admin/advanced/response_templates/:id/edit**: Ensures correct behavior under the specified conditions
- **PATCH /admin/advanced/response_templates/:id**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: renders with status 200

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders with status 200

### S-2: renders with status 200

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders with status 200

### S-3: renders with status 200

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders with status 200

### S-4: renders with status 200

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders with status 200

### S-5: successfully creates a response template

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** successfully creates a response template

### S-6: shows a proper error message if the request was invalid

- **Given** the request was invalid
- **When** the action is triggered
- **Then** shows a proper error message

### S-7: renders successfully if a valid response template was found

- **Given** a valid response template was found
- **When** the action is triggered
- **Then** renders successfully

### S-8: renders the response template

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the response template

### S-9: successfully updates with a valid request

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** successfully updates with a valid request

### S-10: renders an error if the request was invalid

- **Given** the request was invalid
- **When** the action is triggered
- **Then** renders an error

### S-11: successfully deletes the response template

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** successfully deletes the response template

