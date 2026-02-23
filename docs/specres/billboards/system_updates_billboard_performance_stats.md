---
id: "01KJ6EAVZ4S2WVA6ZG0R9DPDZS"
name: "system_updates_billboard_performance_stats"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/workers/billboards/data_update_worker.rb`
- `app/models/billboard.rb`
- `spec/workers/billboards/data_update_worker_spec.rb` (Test)

## Functional Overview

`Billboards::DataUpdateWorker` is a low-priority Sidekiq job that recalculates performance metrics (impressions, clicks, and success rate) for a single billboard. It is enqueued asynchronously when a billboard receives a new event (via `ThrottledCall` from the events controller) or when a live billboard is taken down (via an `after_save` callback in `Billboard`). Before recalculating metrics, the worker always calls `check_and_handle_expiration` on the billboard to auto-unapprove it if its `expires_at` date has passed. For high-impression billboards the worker probabilistically skips the metric update to reduce database load. When it does proceed, it either performs a full aggregation of all historical events (if no prior tabulation exists) or an incremental aggregation of only events created since the last `counts_tabulated_at` timestamp. Conversion events are weighted by a `CONVERSION_SUCCESS_MODIFIER` of 25 before being added to clicks in the success rate formula.

## Design Intent

Incremental counting (using `counts_tabulated_at` as a cutoff) avoids re-scanning the entire event history on every run, keeping queries cheap as event volume grows. The probabilistic skip for billboards with more than 100k or 500k impressions further reduces database pressure: very popular billboards already have statistically stable rates and do not need recalculation on every event. The `CONVERSION_SUCCESS_MODIFIER` (25x) amplifies conversion events in the success rate formula so that high-value conversion actions have a stronger influence on ad ranking than raw clicks alone.

## Key Members

- `CONVERSION_SUCCESS_MODIFIER` — integer constant (25) that multiplies conversion event counts before they are combined with clicks in the success rate formula.
- `counts_tabulated_at` — timestamp recorded on the billboard after each successful update run; used as the lower-bound cutoff for incremental event aggregation.
- `success_rate` — stored float computed as `(clicks + conversion_weight) / impressions`; used downstream for weighted ad selection.

## Scenarios

### First-time full aggregation

1. The worker receives a billboard ID for a billboard whose `counts_tabulated_at` is nil.
2. The worker calls `check_and_handle_expiration`; if the billboard has not expired, it continues.
3. The worker sums all impression, click, and conversion events across the billboard's entire event history.
4. Conversion totals are multiplied by 25 and added to total clicks to compute the success rate numerator.
5. The billboard's `impressions_count`, `clicks_count`, `success_rate`, and `counts_tabulated_at` are all written atomically via `update_columns`.

### Incremental update after prior tabulation

1. The worker receives a billboard ID for a billboard that already has a `counts_tabulated_at` value.
2. The worker calls `check_and_handle_expiration` and continues if the billboard has not expired.
3. The worker queries only events created after `counts_tabulated_at` to obtain the new impression, click, and conversion deltas.
4. The deltas are added to the existing stored counts; the weighted conversion delta is added to the new click total for the success rate numerator.
5. The billboard record is updated with the new cumulative totals and `counts_tabulated_at` is advanced to the current timestamp.

### Probabilistic skip for very high-impression billboards (>500k)

1. After expiration handling, the worker samples `rand(3)`.
2. If the result is greater than 0 and the billboard has more than 500,000 impressions, the worker returns immediately without updating any metrics.

### Probabilistic skip for moderately high-impression billboards (>100k)

1. If the billboard passes the first probabilistic check, the worker samples `rand(2)`.
2. If the result is zero and the billboard has more than 100,000 impressions, the worker returns immediately without updating any metrics.

### Auto-unapprove on expiration

1. At the start of every run, the worker calls `check_and_handle_expiration` on the billboard.
2. If the billboard's `expires_at` is in the past and it is currently approved, it is marked not approved via `update_column`.
3. The metric update then proceeds (or is skipped probabilistically) regardless of whether expiration was triggered.

## Failures / Exceptions

- If the billboard record does not exist for the given ID, `Billboard.find` raises `ActiveRecord::RecordNotFound`, and the job will retry up to 10 times per its `sidekiq_options` configuration.
- Division by zero in the success rate formula is possible if `impressions_count` is zero after a full aggregation; the code does not guard against this explicitly.
