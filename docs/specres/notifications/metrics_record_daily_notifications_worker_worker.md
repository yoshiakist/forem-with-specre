---
id: "01KHY7Q085BDD2KDBTH0PEC0NX"
name: "metrics_record_daily_notifications_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/metrics/record_daily_notifications_worker.rb
- spec/workers/metrics/record_daily_notifications_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Metrics::RecordDailyNotificationsWorker` within the notifications domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/metrics/record_daily_notifications_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: logs welcome notification click events created in the past day

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs welcome notification click events created in the past day

