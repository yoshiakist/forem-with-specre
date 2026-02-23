---
id: "01KJ6EB6TC32BW8DSXN5DVWY9M"
name: "system_rolls_up_billboard_events"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/services/billboard_event_rollup.rb`
- `app/workers/billboard_event_rollup_worker.rb`
- `app/models/billboard_event.rb`
- `spec/services/billboard_event_rollup_spec.rb` (Test)
- `spec/workers/billboard_event_rollup_worker_spec.rb` (Test)

## Functional Overview

The system periodically compacts duplicate `BillboardEvent` records to reduce database storage. A background worker running on the `low_priority` Sidekiq queue triggers the rollup each time it runs, targeting events from 32 days ago. The service fetches all distinct billboard IDs active on that date, then for each billboard loads its events and groups them by the four-tuple `(user_id, display_ad_id, category, context_type)`. Any group containing two or more events is replaced atomically: a single new compacted record is created with a `counts_for` value equal to the sum of all events in the group, and the original records are deleted. Groups of exactly one event are left untouched. Each billboard is processed inside its own savepoint transaction, and every database operation is guarded by a configurable `statement_timeout` to prevent long-running queries from blocking the database.

## Design Intent

Events are grouped by four dimensions — user identity, billboard, interaction category, and display context — so that the compacted record preserves the same analytical granularity as the originals. Processing one billboard per transaction limits the blast radius of a timeout or error to a single billboard rather than the entire rollup run. The `EventAggregator` uses a four-level nested auto-vivifying hash so that grouping requires no sorting, joining, or intermediate collections. The `counts_for` field allows previously compacted records (whose value may already be greater than 1) to be re-compacted correctly by summing rather than counting.

## Key Members

- `STATEMENT_TIMEOUT` — duration (in seconds, as a float) applied to each database query, sourced from the `STATEMENT_TIMEOUT_BULK_DELETE` environment variable with a default of 10 000 ms.
- `ATTRIBUTES_PRESERVED` — `[:user_id, :display_ad_id, :category, :context_type, :created_at]`: fields carried over to the compacted record.
- `ATTRIBUTES_DESTROYED` — `[:id, :counts_for, :updated_at, :article_id, :geolocation]`: fields discarded during compaction (counts_for is replaced by the aggregate sum).
- `EventAggregator` — inner class that accumulates events into a four-level nested hash and yields only groups of size ≥ 2 as `Compact` structs.

## Scenarios

### Worker schedules rollup for 32 days ago

1. The `BillboardEventRollupWorker` is executed by Sidekiq on the `low_priority` queue.
2. The worker calculates the target date as the current date minus 32 days.
3. It calls `BillboardEventRollup.rollup` with that date and returns.

### Service collects distinct billboards and iterates

1. The rollup service queries `BillboardEvent` for all events whose `created_at` falls within the target date (full day range), applying a statement timeout.
2. It extracts the distinct set of `display_ad_id` values from those events.
3. For each `display_ad_id`, it opens a savepoint transaction and loads all events for that billboard on that date in batches of 1 000.

### Groups of duplicate events are compacted into one record

1. Within each billboard's transaction, events are fed into `EventAggregator`, which buckets them by `(user_id, display_ad_id, category, context_type)`.
2. For every bucket that contains two or more events, the aggregator yields a `Compact` struct carrying those events and the shared key fields.
3. The service opens an inner transaction for each compact group: it creates a new `BillboardEvent` with `counts_for` set to the sum of the group's individual `counts_for` values and `created_at` taken from the first event, then deletes all original records in that group.
4. The newly created compacted record is collected and returned by the rollup call.

### Groups with only one event are left unchanged

1. An event group that contains exactly one record is skipped by `EventAggregator`.
2. No new record is created and the existing record is not deleted.

### Statement timeout is set and reset around every query

1. Before the initial query for distinct billboard IDs, the service sets a session-level statement timeout.
2. After the query completes (or if it times out), the timeout is reset.
3. Inside each billboard transaction, a transaction-local statement timeout is set via `SET LOCAL`, and reset in an `ensure` block so it is always cleared regardless of success or failure.
4. Inside each inner compaction transaction, the same local timeout pattern is applied.

## Failures / Exceptions

- If a statement timeout is exceeded during the initial billboard ID query, the exception propagates to the caller; the `RESET statement_timeout` executes before the error surfaces due to the sequential call pattern.
- If a timeout or error occurs during a billboard's savepoint transaction, only that billboard's changes are rolled back; other billboards already processed in the same run are unaffected.
- The `ATTRIBUTES_PRESERVED` + `ATTRIBUTES_DESTROYED` lists must collectively match every column on `display_ad_events`; a spec asserts this invariant so that newly added columns are not silently dropped during compaction.
