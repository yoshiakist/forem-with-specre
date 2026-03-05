---
id: "01KJ164X04NVKMCJE01KSRGXV2"
name: "system_records_daily_notification_metrics"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/workers/metrics/record_daily_notifications_worker.rb`
- `spec/workers/metrics/record_daily_notifications_worker_spec.rb` (Test)

## Functional Overview

`Metrics::RecordDailyNotificationsWorker` is a Sidekiq background job that runs on the low-priority queue and collects daily click-through metrics for welcome notifications. For each of eleven predefined welcome notification titles, it queries the Ahoy analytics event store for "Clicked Welcome Notification" events that occurred in the past 24 hours and filtered by that title, then emits the resulting count to the stats client under the `ahoy_events` metric key tagged with the notification title.

## Design Intent

Iterating over a fixed, exhaustive list of known notification titles (rather than grouping dynamically) ensures that every title is always reported, even when its count is zero, giving time-series monitoring tools a consistent set of series to track and alert on.

## Key Members

- `EVENT_TITLES` — A frozen array of eleven known welcome notification title strings used to filter and tag individual metric emissions.

## Scenarios

### Recording daily click counts per notification title

1. The worker's `perform` method is invoked by Sidekiq.
2. For each title in `EVENT_TITLES`, the system queries `Ahoy::Event` for records named "Clicked Welcome Notification" whose `time` is within the past day and whose `title` property matches the current title.
3. The count of matching events is emitted to `ForemStatsClient` as an `ahoy_events` metric with a tag in the form `title:<notification_title>`.
4. This repeats for all eleven titles in sequence before the job completes.

### Enqueueing on the correct queue

1. When the worker is enqueued, Sidekiq places it on the `low_priority` queue with up to 10 retries on failure.
