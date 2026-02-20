---
id: "01KHYAKB75F6053BFGHPDYQ04A"
name: "organization_tracks_promotional_billboard_impressions"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/organizations/track_promotional_billboard_impressions_worker.rb
- spec/workers/organizations/track_promotional_billboard_impressions_worker_spec.rb (Test)

## Functional Overview

The TrackPromotionalBillboardImpressionsWorker is a low-priority, throttled Sidekiq job that aggregates promotional billboard impressions over the past 24 hours per organization, updates cached impression counts, and pauses promotional billboards when impressions exceed twice the ideal daily threshold.

## Scenarios

### Worker aggregates impressions and updates organizations

1. The worker uses a read-only database connection with a configurable statement timeout.
2. The worker executes a single aggregate SQL query to sum billboard impression events grouped by organization ID for the past 24 hours.
3. For each organization with `ideal_daily_promoted_billboard_impressions > 0`, the worker updates the `past_24_hours_promoted_billboard_impressions` column.

### Worker pauses billboards when threshold exceeded

1. If an organization's past 24 hours impressions exceed twice its `ideal_daily_promoted_billboard_impressions`, the worker sets `currently_paused_promotional_billboards` to true.
2. The worker caches the list of paused organization IDs under a fixed cache key with a 15-minute expiry.
3. The class method `paused_organization_ids` reads the cached list, returning an empty array if not cached.

### Worker handles errors gracefully

1. If processing a single organization fails, the worker logs the error and continues to the next organization.
2. If the entire query times out (QueryCanceled), the worker logs the error and re-raises to trigger Sidekiq retry.
3. The worker is throttled to a concurrency of 1 and configured for up to 3 retries.

## Key Members

- `ideal_daily_promoted_billboard_impressions`: Per-organization threshold for daily impressions.
- `currently_paused_promotional_billboards`: Boolean flag set when impressions exceed 2x threshold.
- `CACHE_KEY`: "paused_promotional_billboard_organization_ids" — stores paused org IDs for 15 minutes.
