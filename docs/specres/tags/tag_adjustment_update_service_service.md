---
id: "01KHY7Q0C8A6XR1392A6DME8QP"
name: "tag_adjustment_update_service_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/tag_adjustment_update_service.rb
- app/services/notifications/tag_adjustment_notification/send.rb
- app/services/tag_adjustment_creation_service.rb
- spec/services/tag_adjustment_update_service_spec.rb

## Functional Overview

This specification defines the expected behavior of `TagAdjustmentUpdateService` within the tags domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/tag_adjustment_update_service.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/tag_adjustment_notification/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/tag_adjustment_creation_service.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: creates tag adjustment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates tag adjustment

