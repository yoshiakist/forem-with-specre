---
id: "01KJBV8Z82V16HGEYRAJK0CCHN"
name: "system_tracks_article_reading_time"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/javascript/packs/baseTracking.js` (shared with `system_records_article_page_view` / `01KJBV508Z7X8FZ7BZP7XQNTN1`)
- `app/controllers/page_views_controller.rb` (shared with `system_records_article_page_view` / `01KJBV508Z7X8FZ7BZP7XQNTN1`)
- `app/services/articles/page_view_updater.rb`
- `spec/services/articles/page_view_updater_spec.rb` (Test)
- `spec/requests/page_views_spec.rb` (Test, shared with `system_records_article_page_view` / `01KJBV508Z7X8FZ7BZP7XQNTN1`)

## Functional Overview

After a user has been on an article page for at least 15 seconds, the browser begins firing a recurring PATCH request to the page views endpoint every 15 seconds. Each request causes the server to increment the `time_tracked_in_seconds` field on the corresponding `PageView` record by 15. Views for unpublished articles and self-authored articles are silently ignored. Once the cumulative reading time reaches exactly 60 seconds (`EXTENDED_PAGEVIEW_NUMBER`), the system records an `extended_pageview` feed event to signal deep engagement with the article.

## Design Intent

Tracking is intentionally incremental (15-second ticks) rather than reporting a final duration, so that partial reading sessions are captured even if the user closes the tab before a longer threshold is met. The 60-second milestone is treated as a one-time signal of extended engagement rather than a continuously growing counter, ensuring that each deep-read is recorded exactly once per `PageView` record.

## Key Members

- `EXTENDED_PAGEVIEW_NUMBER` (60) — the cumulative seconds threshold at which an `extended_pageview` feed event is emitted
- `time_tracked_in_seconds` — integer column on `PageView` that accumulates reading time in 15-second increments
- `timeOnSiteInterval` — client-side interval (15 000 ms) that drives periodic PATCH calls; stops after ~118 ticks (~30 minutes) or when the article element is no longer present

## Scenarios

### Timer fires while a logged-in user reads a published article by another author

1. After the page loads, the browser waits 15 seconds and then fires a PATCH request to `/page_views/:article_id` every 15 seconds as long as the article element is visible and the user is logged in.
2. The server's `update` action receives the request, identifies the current user from the session, and delegates to `Articles::PageViewUpdater`.
3. The updater locates the most-recently-created `PageView` for the article–user pair (creating one if it does not exist yet) and increments `time_tracked_in_seconds` by 15.
4. The response is `200 OK` with no body.

### Cumulative reading time reaches 60 seconds

1. The client fires enough PATCH requests that `time_tracked_in_seconds` on the `PageView` is incremented from 45 to 60.
2. The updater detects that the new value equals `EXTENDED_PAGEVIEW_NUMBER` and records an `extended_pageview` feed event for the user and article via `FeedEvent.record_journey_for`.
3. On subsequent PATCH calls the counter continues to climb past 60, but no additional extended-pageview events are emitted.

### User is not logged in

1. A PATCH request arrives at the `update` action with no session user.
2. The controller skips the call to `Articles::PageViewUpdater` entirely.
3. The response is still `200 OK` and the `PageView` record is not modified.

### Article is unpublished or authored by the requesting user

1. `Articles::PageViewUpdater` is called with the article and user IDs.
2. If the article is unpublished, or if the article's author matches the requesting user, the updater returns `false` immediately without touching any `PageView` record.

### Timer stops after prolonged reading

1. The client-side interval increments an internal counter on each tick.
2. When the counter exceeds 118 (approximately 30 minutes of continuous reading), the interval is cleared and no further PATCH requests are sent.

## Failures / Exceptions

- An invalid article ID (e.g., one that does not correspond to any `PageView`) causes the updater to attempt a `find_or_create_by` that either finds nothing or creates a new record; the controller rescues by returning `200 OK` regardless, so no error propagates to the client.
