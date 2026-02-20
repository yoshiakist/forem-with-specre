---
id: "01KHY7Q0ZBMC819NNZ9114TAQW"
name: "page_view_rollup_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/page_view_rollup.rb
- app/workers/page_view_rollup_worker.rb
- app/services/analytics_service.rb
- app/services/articles/page_view_updater.rb
- spec/services/page_view_rollup_spec.rb

## Functional Overview

This specification defines the expected behavior of `PageViewRollup` within the analytics domain.

### Behavioral Areas

- **when compacting many rows**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/page_view_rollup.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/page_view_rollup_worker.rb` -- asynchronous job processing
- **Service layer**: `app/services/analytics_service.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/page_view_updater.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: fails if new attributes would be lost

- **Given** new attributes would be lost
- **When** the action is triggered
- **Then** fails

### S-2: does not compact signed-in user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not compact signed-in user

### S-3: compacts by the hour

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** compacts by the hour

### S-4: does not compact views outside of the same hour

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not compact views outside of the same hour

### S-5: only compacts views of the same article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** only compacts views of the same article

