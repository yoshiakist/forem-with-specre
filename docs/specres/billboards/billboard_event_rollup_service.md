---
id: "01KHY7Q0XRJF9XPG7074VS8CCZ"
name: "billboard_event_rollup_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/billboard_event_rollup.rb
- app/workers/billboard_event_rollup_worker.rb
- spec/services/billboard_event_rollup_spec.rb

## Functional Overview

This specification defines the expected behavior of `BillboardEventRollup` within the billboards domain.

### Behavioral Areas

- **when compacting many rows**: handles statement timeout when compacting records

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/billboard_event_rollup.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/billboard_event_rollup_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: handles statement timeout when compacting records

- **Given** the system is in a standard operational state
- **When** compacting records
- **Then** handles statement timeout

### S-2: fails if new attributes would be lost

- **Given** new attributes would be lost
- **When** the action is triggered
- **Then** fails

### S-3: compacts one day

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** compacts one day

### S-4: groups by category

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** groups by category

### S-5: groups by billboard_id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** groups by billboard_id

### S-6: groups by user_id (including null / logged-out user)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** groups by user_id (including null / logged-out user)

### S-7: counts previously crunched

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** counts previously crunched

