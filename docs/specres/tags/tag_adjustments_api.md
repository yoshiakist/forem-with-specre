---
id: "01KHY7Q0BXC7M7AQP62DW0QT1G"
name: "tag_adjustments_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/tag_adjustments_controller.rb
- spec/requests/tag_adjustments_spec.rb

## Functional Overview

This specification defines the expected behavior of `"TagAdjustments"` within the tags domain.

### Behavioral Areas

- **TagAdjustments**: Ensures correct behavior under the specified conditions
- **POST /tag_adjustments**: Ensures correct behavior under the specified conditions
- **when an article doesn**: Ensures correct behavior under the specified conditions
- **when an article uses front matter**: Ensures correct behavior under the specified conditions
- **POST /tag_adjustments with adjustment_type addition**: Ensures correct behavior under the specified conditions
- **when an article doesn**: Ensures correct behavior under the specified conditions
- **when an article uses front matter**: Ensures correct behavior under the specified conditions
- **DELETE /tag_adjustments/:id**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/tag_adjustments_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: removes the tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes the tag

### S-2: keeps the other tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** keeps the other tags

### S-3: removes the tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes the tag

### S-4: keeps the other tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** keeps the other tags

### S-5: adds the tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds the tag

### S-6: keeps the other tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** keeps the other tags

### S-7: adds the tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds the tag

### S-8: keeps the other tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** keeps the other tags

### S-9: adds the tag back in

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds the tag back in

### S-10: adds the tag back in

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds the tag back in

### S-11: removes the added tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes the added tag

### S-12: removes the added tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes the added tag

