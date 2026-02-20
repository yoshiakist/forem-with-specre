---
id: "01KHY7PZYXVW7R8JJ9RQSE9CH8"
name: "segmented_users_bulk_delete_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/segmented_users/bulk_delete.rb
- app/services/segmented_users/bulk_upsert.rb
- spec/services/segmented_users/bulk_delete_spec.rb

## Functional Overview

This specification defines the expected behavior of `SegmentedUsers::BulkDelete` within the users domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/segmented_users/bulk_delete.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/segmented_users/bulk_upsert.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: removes only the passed users from the segment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes only the passed users from the segment

### S-2: gracefully handles users that don

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** gracefully handles users that don

