---
id: "01KHY7Q1HKAJW8KDC9ETAY9F69"
name: "invitations_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/invitations_controller.rb
- app/controllers/invitations_controller.rb
- spec/requests/invitations_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Invitations"` within the invitations domain.

### Behavioral Areas

- **Invitations**: Ensures correct behavior under the specified conditions
- **Accept invitation**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/invitations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/invitations_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: renders normal response even if the Forem instance is private

- **Given** the Forem instance is private
- **When** the action is triggered
- **Then** renders normal response even

