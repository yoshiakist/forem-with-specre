---
id: "01KHY7Q0XXQFY86JV12NJ8K4B7"
name: "billboards_data_update_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/billboards/data_update_worker.rb
- app/controllers/admin/billboards_controller.rb
- app/controllers/api/v1/billboards_controller.rb
- app/controllers/billboards_controller.rb
- app/queries/billboards/filtered_ads_query.rb
- app/workers/billboards/track_email_click_worker.rb
- spec/workers/billboards/data_update_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Billboards::DataUpdateWorker` within the billboards domain.

### Behavioral Areas

- **perform_update**: Ensures correct behavior under the specified conditions
- **when the billboard has never been tabulated before**: does not change the billboard at all
- **when the billboard has been tabulated before**: does not change the billboard at all
- **when impressions_count is very large and first random check triggers early return**: handles expiration when billboard has expired
- **when impressions_count is above 100_000 but below 500_000 and second random check triggers early return**: handles expiration when billboard has expired
- **when handling billboard expiration**: does not change the billboard at all
- **when billboard has expired**: does not change the billboard at all
- **when billboard has not expired**: does not change the billboard at all

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/billboards/data_update_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/billboards_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/billboards_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/billboards_controller.rb` -- HTTP request routing and response handling
- **Query object**: `app/queries/billboards/filtered_ads_query.rb` -- complex database query encapsulation
- **Background worker**: `app/workers/billboards/track_email_click_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: aggregates all events and updates counts / rate / tabulation timestamp

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** aggregates all events and updates counts / rate / tabulation timestamp

### S-2: aggregates only new events and increments counters accordingly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** aggregates only new events and increments counters accordingly

### S-3: does not change the billboard at all

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not change the billboard at all

### S-4: does not change the billboard at all

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not change the billboard at all

### S-5: handles expiration when billboard has expired

- **Given** the system is in a standard operational state
- **When** billboard has expired
- **Then** handles expiration

### S-6: marks the billboard as not approved

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** marks the billboard as not approved

### S-7: still processes other updates normally

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** still processes other updates normally

### S-8: does not change the billboard approval status

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not change the billboard approval status

### S-9: does not change the billboard approval status

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not change the billboard approval status

