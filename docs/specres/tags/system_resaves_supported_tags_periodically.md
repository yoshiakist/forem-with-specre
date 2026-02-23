---
id: "01KJ41NM38SFJ4PT77ZR180XVP"
name: "system_resaves_supported_tags_periodically"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/workers/tags/resave_supported_tags_worker.rb`
- `spec/workers/tags/resave_supported_tags_worker_spec.rb` (Test)

## Functional Overview

`Tags::ResaveSupportedTagsWorker` is a background job that periodically re-saves every supported tag and refreshes scores for every subforem. When performed, it iterates over all `Tag` records marked as supported and calls `save` on each, which triggers ActiveRecord callbacks and updates timestamps. It then iterates over all `Subforem` records and calls `update_scores!` on each. The job runs on the `low_priority` queue, retries up to five times on failure, and is throttled to a concurrency limit of one to prevent overlapping runs.

## Design Intent

Re-saving each supported tag triggers any ActiveRecord `after_save` callbacks that maintain derived data (such as cached counts or search index entries) without requiring explicit logic in the worker itself. The concurrency throttle of one ensures that two runs of this job do not overlap and cause redundant or conflicting writes.

## Scenarios

### Worker is enqueued and performs normally

1. The scheduler enqueues `Tags::ResaveSupportedTagsWorker` on the `low_priority` queue.
2. Sidekiq picks up the job; the concurrency throttle ensures no other instance of this worker runs simultaneously.
3. The worker retrieves all `Tag` records where `supported` is true, iterating in batches.
4. Each supported tag is re-saved, causing ActiveRecord to run its callbacks and update the record's `updated_at` timestamp.
5. The worker then iterates over every `Subforem` record in batches and calls `update_scores!` on each.
6. The job completes successfully.

### Job fails and is retried

1. An exception is raised during the save loop (for example, a database timeout).
2. Sidekiq marks the job as failed and schedules a retry.
3. The job is retried up to five times according to the `retry: 5` option.
4. Once the transient error resolves, a subsequent retry completes successfully.
