---
id: "01KJ6EE9EXCHR36PGTH6Y1239R"
name: "system_tracks_billboard_email_clicks"
status: "draft"
---

## Related Files

- `app/workers/billboards/track_email_click_worker.rb`
- `app/models/billboard_event.rb`

## Functional Overview

When a user clicks a billboard link inside a digest email, the system enqueues a background job (`Billboards::TrackEmailClickWorker`) that records the interaction as a `BillboardEvent` with category "click" and context_type "email". After persisting the event, the job recalculates and updates the billboard's aggregate performance metrics — total impressions, total clicks, and success rate — directly on the billboard record. The write is executed inside a `with_synchronous_commit_off` block for performance. The associated user is resolved from the provided user ID and may be nil (anonymous). Any error raised during processing is caught and logged rather than re-raised, so the job does not retry on application errors.

## Design Intent

Using a low-priority Sidekiq queue with `retry: 10` keeps email click tracking out of the critical path while still ensuring eventual consistency for the metrics. The `with_synchronous_commit_off` block reduces I/O wait by allowing the database to flush the commit asynchronously, which is acceptable for analytics data that does not require immediate durability guarantees. Swallowing `StandardError` and logging instead of re-raising prevents the job from consuming retry budget on deterministic failures (e.g., a permanently invalid billboard ID).

## Key Members

- `bb_param` — the billboard ID passed as a string or integer; coerced to integer with `to_i` before use.
- `user_id` — the ID of the user who clicked; resolved to a `User` record via `find_by` so that deleted users result in a nil association rather than an error.
- `BillboardEvent#category` — must be one of the `VALID_CATEGORIES` constants; this job always sets it to `"click"`.
- `BillboardEvent#context_type` — must be one of the `VALID_CONTEXT_TYPES` constants; this job always sets it to `"email"`.
- `billboard.success_rate` — recomputed as `clicks / impressions`; set to 0 when there are no impressions.

## Scenarios

### User clicks a billboard link in an email

1. The system enqueues `Billboards::TrackEmailClickWorker` with the billboard's ID and the clicking user's ID.
2. The worker resolves the user record from the given ID (the user may no longer exist).
3. Inside a non-blocking commit block, the worker creates a `BillboardEvent` with category "click" and context_type "email", associating the billboard and the user (if present).
4. The worker fetches the billboard record, sums all impression and click event counts, computes the success rate, and writes the updated figures back to the billboard.
5. The billboard's `impressions_count`, `clicks_count`, and `success_rate` columns reflect the new totals.

### Billboard no longer exists at processing time

1. The worker creates the `BillboardEvent` record successfully.
2. When attempting to update billboard counts, `Billboard.find_by` returns nil.
3. The update step is skipped; no error is raised.

### An error occurs during event creation or metric update

1. A `StandardError` is raised at any point inside the tracking block.
2. The worker catches the error, logs a message containing the error details, and exits without re-raising.
3. No Sidekiq retry is triggered for this execution; the normal Sidekiq retry policy handles upstream infrastructure failures separately.

## Failures / Exceptions

- If `Billboard.find_by` returns nil (billboard deleted), the metric update is silently skipped.
- If any `StandardError` is raised during event creation or metric calculation, the error is logged via `Rails.logger.error` and the job terminates without propagating the exception.
