---
id: "01KJ02RGJEYQ75XMH5YJ3321SK"
name: "system_tracks_organization_billboard_impressions"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/workers/organizations/track_promotional_billboard_impressions_worker.rb`
- `spec/workers/organizations/track_promotional_billboard_impressions_worker_spec.rb` (Test)

## Functional Overview

A background worker runs periodically to count how many promotional billboard impressions each organization has received in the past 24 hours. It queries billboard impression events from the read-only database in a single aggregate query, updates each eligible organization's 24-hour impression count, and then pauses promotional billboards for any organization whose impression count exceeds twice its configured ideal daily target. The IDs of currently paused organizations are written to a short-lived cache entry so that other parts of the system can quickly determine which organizations are paused without hitting the database.

## Design Intent

The worker uses the read-only database replica to avoid putting load on the primary database during the aggregation query. A single SQL aggregate query groups all impression events by organization, replacing what would otherwise be one query per organization (an N+1 pattern). The pause threshold is set at strictly greater than 2x the ideal daily amount — hitting exactly 2x does not trigger a pause — giving organizations a comfortable buffer before their promotional content is suppressed. Individual organization processing errors are caught and logged without stopping the rest of the batch. The cache TTL of 15 minutes means pause state is eventually consistent rather than perfectly real-time.

## Key Members

- `ideal_daily_promoted_billboard_impressions` — the configured daily target impression count for an organization; organizations with a value of zero or nil are excluded from tracking
- `past_24_hours_promoted_billboard_impressions` — the rolling 24-hour impression count written to the organization record on each worker run
- `currently_paused_promotional_billboards` — boolean flag on the organization record indicating whether promotional billboards are currently suppressed
- `CACHE_KEY` (`"paused_promotional_billboard_organization_ids"`) — the Rails cache key under which paused organization IDs are stored
- `CACHE_EXPIRY` (15 minutes) — how long the paused-IDs cache entry remains valid
- `STATEMENT_TIMEOUT` — maximum milliseconds the aggregate SQL query is allowed to run before being cancelled (defaults to 30,000 ms, overridable via `STATEMENT_TIMEOUT_BULK_DELETE` env var)

## Scenarios

### Normal run — impressions within limit

1. The worker is enqueued by Sidekiq on the low-priority queue.
2. It opens a read-only database connection and begins a transaction with the configured statement timeout.
3. It fetches the total impression counts for all organizations in a single SQL query, summing only `impression`-category events created in the past 24 hours and joined to their parent billboard's organization.
4. It queries all organizations whose `ideal_daily_promoted_billboard_impressions` is greater than zero.
5. For each such organization, the worker writes the 24-hour impression count to `past_24_hours_promoted_billboard_impressions`.
6. Because the count does not exceed twice the ideal daily target, `currently_paused_promotional_billboards` is set to `false`.
7. After processing all organizations, the worker writes an empty array (no paused IDs) to the cache with a 15-minute expiry.

### Impressions exceed 2x ideal daily — organization is paused

1. Steps 1–5 proceed as in the normal run.
2. The 24-hour impression count is strictly greater than twice `ideal_daily_promoted_billboard_impressions`.
3. `currently_paused_promotional_billboards` is set to `true` for that organization.
4. The organization's ID is added to the list of paused IDs.
5. After the full batch, the deduplicated list of paused organization IDs is written to the cache with a 15-minute expiry.

### Impressions exactly equal 2x ideal daily — organization is not paused

1. Steps 1–5 proceed as in the normal run.
2. The 24-hour impression count equals exactly twice `ideal_daily_promoted_billboard_impressions`.
3. The pause condition requires the count to be *strictly greater than* 2x; equality does not satisfy it.
4. `currently_paused_promotional_billboards` is set to `false` and the organization is not added to the paused list.

### Organization transitions from paused back to active

1. An organization's `currently_paused_promotional_billboards` is currently `true` and its ID is in the cache.
2. The worker runs and finds the current 24-hour impression count is no longer above the 2x threshold.
3. `currently_paused_promotional_billboards` is set to `false`.
4. The organization's ID is not included in the new paused list written to cache.

### Organization has tracking disabled

1. An organization's `ideal_daily_promoted_billboard_impressions` is zero or nil.
2. The worker's initial query excludes this organization entirely.
3. No impression count or pause state is updated for that organization.

### Multiple billboards for the same organization

1. An organization has more than one promotional billboard, each accumulating impression events.
2. The aggregate SQL query groups by `organization_id` and sums `counts_for` across all billboards belonging to that organization.
3. The single combined total is written to `past_24_hours_promoted_billboard_impressions`.

### Only impression events are counted

1. An organization's billboards have events of categories `impression`, `click`, and `conversion`.
2. The SQL query filters exclusively on `category = 'impression'`.
3. Click and conversion events are not included in the 24-hour count.

### Cache read via `.paused_organization_ids`

1. Another part of the system calls `TrackPromotionalBillboardImpressionsWorker.paused_organization_ids`.
2. If the cache entry is present and non-empty, the method returns the stored IDs as an array of integers.
3. If the cache entry is absent or empty, the method returns an empty array without querying the database.

### Cache refresh overwrites stale data

1. The cache holds an outdated list of paused organization IDs from a previous run.
2. The worker completes a new run and writes the current paused IDs to the same cache key, replacing the stale data.
3. Subsequent calls to `.paused_organization_ids` return the fresh list.

## Failures / Exceptions

- If processing a single organization raises a `StandardError`, the error and backtrace are logged and the worker continues with the remaining organizations rather than aborting the entire batch.
- If the aggregate SQL query exceeds `STATEMENT_TIMEOUT`, an `ActiveRecord::QueryCanceled` exception is raised. The worker logs the timeout message and re-raises the exception so Sidekiq can retry the job (up to 3 times).
- Concurrency is capped at 1 simultaneous instance via `Sidekiq::Throttled::Job` to prevent overlapping runs from writing conflicting cache values.
