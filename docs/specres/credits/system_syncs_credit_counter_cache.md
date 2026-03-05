---
id: "01KJ2SJQYZE780NB4SYY4CMW9G"
name: "system_syncs_credit_counter_cache"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/workers/credits/sync_counter_cache.rb`
- `spec/workers/credits/sync_counter_cache_spec.rb` (Test)

## Functional Overview

`Credits::SyncCounterCache` is a background worker that repairs potentially out-of-sync credit count caches. It runs on the `low_priority` queue and, when executed, calls `Credit.counter_culture_fix_counts` scoped to the `user` and `organization` associations. This corrects cached credit totals for those two owner types without touching other associations, ensuring that denormalized counters stay consistent with the underlying credit records.

## Design Intent

The worker is scoped to only `user` and `organization` rather than all associations to limit the repair surface to the two owner types that actually store credits. Running it on the `low_priority` queue prevents it from competing with user-facing work, and the `retry: 10` option provides resilience against transient database issues.

## Scenarios

### Counter cache is refreshed for users and organizations

1. A scheduled or manually enqueued job triggers `Credits::SyncCounterCache#perform`.
2. The worker calls `Credit.counter_culture_fix_counts` restricted to the `user` and `organization` associations.
3. The `counter_culture` library queries the actual credit counts from the database and updates the cached counter columns on the `users` and `organizations` tables to match.
4. The job completes with no return value; any previously drifted counters are now accurate.

### Worker is routed to the correct queue

1. When `Credits::SyncCounterCache` is enqueued, Sidekiq places it on the `low_priority` queue as declared by `sidekiq_options`.
2. If the job raises an error it is retried up to 10 times before being moved to the dead queue.
