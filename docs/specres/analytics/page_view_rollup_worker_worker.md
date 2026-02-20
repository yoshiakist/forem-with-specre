---
id: "01KHY7Q0ZGYYZ7CJCRF41V2V6A"
name: "page_view_rollup_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/page_view_rollup_worker.rb
- app/workers/articles/update_organic_page_views_worker.rb
- app/workers/articles/update_page_views_worker.rb
- spec/workers/page_view_rollup_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `PageViewRollupWorker` within the analytics domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/page_view_rollup_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/articles/update_organic_page_views_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/articles/update_page_views_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: rollups five month ago

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rollups five month ago

