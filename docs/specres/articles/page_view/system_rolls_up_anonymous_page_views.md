---
id: "01KJBV15ZA82R2VG3VJ423PZ0H"
name: "system_rolls_up_anonymous_page_views"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/services/page_view_rollup.rb`
- `app/workers/page_view_rollup_worker.rb`
- `spec/services/page_view_rollup_spec.rb` (Test)
- `spec/workers/page_view_rollup_worker_spec.rb` (Test)

## Functional Overview

The system periodically compacts anonymous (non-logged-in) page view records for a given day by merging multiple views of the same article within the same hour into a single aggregated record. The rollup preserves the article association and hour-level timestamp while summing the view count and time-tracked values across the merged records. Authenticated user views are never touched. The `PageViewRollupWorker` Sidekiq job triggers the rollup for one year ago on each run, enqueued on the low-priority queue without retries.

## Design Intent

Rolling up anonymous views reduces database row count over time without losing aggregate metrics. Using a one-hour window as the grouping unit balances granularity against storage savings. Signed-in user views are excluded from compaction so individual user reading history remains intact.

## Key Members

- `ATTRIBUTES_PRESERVED` — columns carried over to the compacted record: `article_id`, `created_at`, `user_id`
- `ATTRIBUTES_DESTROYED` — columns collapsed away during compaction (e.g., `id`, `path`, `referrer`, `user_agent`)
- `ViewAggregator` — internal two-level hash that groups raw view records by `article_id` then `user_id` before compaction
- `Compact` — value object produced by the aggregator that sums `counts_for_number_of_views` and `time_tracked_in_seconds` across all views in the group

## Scenarios

### Rollup compacts multiple anonymous views of the same article within the same hour

1. The worker calls `PageViewRollup.rollup` with a target date (one year ago).
2. For each hour of that day (0–23), the service queries page views with no associated user created within that hour window.
3. Views are grouped by article. Any group containing more than one record is compacted.
4. The service creates a single replacement record whose view count and time-tracked seconds are the sum of all records in the group, timestamped to the start of the hour.
5. The original records in the group are deleted in the same database transaction.
6. The resulting array of created records is returned.

### Views from different hours are not merged together

1. Anonymous views of the same article exist across multiple different hours of the same day.
2. The rollup runs for that day.
3. Each hour is processed independently; views from different hours are never merged, leaving one record per hour per article.

### Authenticated user views are never compacted

1. Both anonymous and signed-in-user views exist for the same article on the target date.
2. The rollup runs.
3. Only anonymous (user_id is nil) records are candidates for compaction; all authenticated user records remain untouched.

### Views of different articles are compacted independently

1. Anonymous views exist for two distinct articles within the same hour of the target date.
2. The rollup runs.
3. Each article's views are compacted separately, producing one aggregated record per article for that hour.

## Failures / Exceptions

- Compaction of each group is wrapped in a database transaction; if either the insert or the delete fails, neither change is persisted for that group.
