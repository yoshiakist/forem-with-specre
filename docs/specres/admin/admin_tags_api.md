---
id: "01KHY7Q13MZXH4YKCMT62ZG7V1"
name: "admin_tags_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/tags_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/content_manager/tags"` within the admin domain.

### Behavioral Areas

- **/admin/content_manager/tags**: Ensures correct behavior under the specified conditions
- **GET /admin/content_manager/tags**: Ensures correct behavior under the specified conditions
- **GET /admin/content_manager/tags/:id**: Ensures correct behavior under the specified conditions
- **POST /admin/content_manager/tags**: updates posts when making a tag an alias for another tag
- **PUT /admin/content_manager/tags**: Ensures correct behavior under the specified conditions
- **when managing subforem relationships**: updates posts when making a tag an alias for another tag


## Scenarios

### S-1: responds with 200 OK

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** responds with 200 OK

### S-2: responds with 200 OK

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** responds with 200 OK

### S-3: creates a new tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new tag

### S-4: updates Tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates Tag

### S-5: updates posts when making a tag an alias for another tag

- **Given** the system is in a standard operational state
- **When** making a tag an alias for another tag
- **Then** updates posts

### S-6: disallows updates to name

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** disallows updates to name

### S-7: creates new subforem relationships for provided subforem_ids

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates new subforem relationships for provided subforem_ids

### S-8: removes subforem relationships not included in subforem_ids

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes subforem relationships not included in subforem_ids

