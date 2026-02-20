---
id: "01KHY7Q0C5T2JPXSWA999BJES2"
name: "tag_adjustment_creation_service_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/tag_adjustment_creation_service.rb
- app/services/notifications/tag_adjustment_notification/send.rb
- app/services/tag_adjustment_update_service.rb
- spec/services/tag_adjustment_creation_service_spec.rb

## Functional Overview

This specification defines the expected behavior of `TagAdjustmentCreationService` within the tags domain.

### Behavioral Areas

- **creates tag adjustment**: with adjustment_type removal
- **creates notification**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/tag_adjustment_creation_service.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/tag_adjustment_notification/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/tag_adjustment_update_service.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: with adjustment_type removal

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** with adjustment_type removal

### S-2: with adjustment_type addition

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** with adjustment_type addition

### S-3: with adjustment_type removal

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** with adjustment_type removal

### S-4: with adjustment_type addition

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** with adjustment_type addition

