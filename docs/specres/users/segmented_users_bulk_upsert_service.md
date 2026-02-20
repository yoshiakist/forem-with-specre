---
id: "01KHY7PZYZAYCKEVVPNVV3KVJF"
name: "segmented_users_bulk_upsert_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/segmented_users/bulk_upsert.rb
- app/services/segmented_users/bulk_delete.rb
- spec/services/segmented_users/bulk_upsert_spec.rb

## Functional Overview

This specification defines the expected behavior of `SegmentedUsers::BulkUpsert` within the users domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/segmented_users/bulk_upsert.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/segmented_users/bulk_delete.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: adds the users to the segment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds the users to the segment

### S-2: retains any existing users in the segment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** retains any existing users in the segment

### S-3: only touches segmented users already in the list

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** only touches segmented users already in the list

### S-4: only touches the segment if any users were successfully upserted

- **Given** any users were successfully upserted
- **When** the action is triggered
- **Then** only touches the segment

### S-5: gracefully handles users that don

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** gracefully handles users that don

### S-6: returns immediately if the segment is not persisted

- **Given** the segment is not persisted
- **When** the action is triggered
- **Then** returns immediately

