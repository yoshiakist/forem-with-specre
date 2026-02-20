---
id: "01KHY7Q0XV4NXHPK3ERWVB4X3R"
name: "billboard_event_rollup_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/billboard_event_rollup_worker.rb
- app/workers/billboards/data_update_worker.rb
- app/workers/billboards/track_email_click_worker.rb
- app/workers/organizations/track_promotional_billboard_impressions_worker.rb
- spec/workers/billboard_event_rollup_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `BillboardEventRollupWorker` within the billboards domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/billboard_event_rollup_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/billboards/data_update_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/billboards/track_email_click_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/organizations/track_promotional_billboard_impressions_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: rollups one month ago

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rollups one month ago

