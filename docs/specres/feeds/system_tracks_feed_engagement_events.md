---
id: "01KJ24DBM92V2E2RDET8BZEWTZ"
name: "system_tracks_feed_engagement_events"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/models/feed_event.rb`
- `app/controllers/feed_events_controller.rb`
- `app/services/feed_events/bulk_upsert.rb`
- `app/javascript/packs/feedEvents.js`
- `spec/models/feed_event_spec.rb` (Test)
- `spec/requests/feed_events_spec.rb` (Test)
- `spec/services/feed_events/bulk_upsert_spec.rb` (Test)

## Functional Overview

The system tracks user engagement with feed articles by recording structured events (impressions, clicks, reactions, comments, and extended pageviews) across the full request lifecycle. In the browser, a `FeedTracker` instance observes feed items via `IntersectionObserver` to queue impression events when items become 25% visible, and listens for mousedown events to capture clicks; batches are sent to `POST /feed_events` via `sendBeacon` or a keepalive fetch fallback. The controller accepts batches only for authenticated users and delegates storage to `FeedEvents::BulkUpsert`, which validates each event, suppresses duplicates within a configurable timebox (default 5 minutes), and bulk-inserts survivors. After each save, the model asynchronously recalculates per-article and per-`FeedConfig` success scores (using distinct-user weighted sums), and triggers a feed-config evolutionary branch whenever a reaction or comment event is recorded.

## Design Intent

Bulk insertion with application-side timebox deduplication is used instead of database-level `ON CONFLICT` upserts because the uniqueness constraint is time-scoped, not absolute — the same user can legitimately click the same article again after the timebox expires. This approach accepts a small race-condition margin in exchange for simpler SQL and avoiding table locks.

Score computation uses distinct user counts (not raw event counts) to prevent inflated metrics from repeated interactions by the same user, and applies different multipliers by category to reflect relative engagement quality (comments are weighted most heavily).

## Key Members

- `FeedEvent#category` (`enum`) — `impression`, `click`, `reaction`, `comment`, `extended_pageview`
- `FeedEvent::VALID_CONTEXT_TYPES` — `home`, `search`, `tag`, `email`, `sidebar`
- `FeedEvent::DEFAULT_TIMEBOX` — 5 minutes; the window within which duplicate events are suppressed
- `FeedEvent::REACTION_SCORE_MULTIPLIER` / `COMMENT_SCORE_MULTIPLIER` — weights applied per distinct engaged user when computing `feed_success_score`
- `FeedTracker` — client-side class managing the event queue, `IntersectionObserver`, and batch submission for a single feed container
- `MAX_BATCH_SIZE` / `AUTOSEND_PERIOD` / `VISIBLE_THRESHOLD` — client-side constants controlling batch size (20), auto-send interval (5 s), and visibility threshold (25%)

## Scenarios

### Client observes and queues a feed impression

1. The page renders a feed and calls `observeFeedElements`, which creates (or reuses) a `window.mainFeedTracker` instance and calls `init`.
2. `FeedTracker` assigns sequential positions to each feed item and registers them with an `IntersectionObserver`.
3. When a feed item becomes at least 25% visible, the observer queues an impression event containing the article id, position, context type, and feed config id.
4. If the queue reaches `MAX_BATCH_SIZE` or `AUTOSEND_PERIOD` elapses, the batch is flushed; on page hide/unload the remaining queue is also sent.

### Client captures and immediately flushes a click event

1. A user presses a mouse button on a tracked feed item.
2. `trackFeedClickListener` queues a click event for that item (once per item per page load).
3. `submitEventsBatch` is called immediately after queuing to send the click without waiting for the next periodic flush, because clicks are high-value signals.

### Server accepts and bulk-inserts a batch of events

1. The browser sends `POST /feed_events` with an array of event objects.
2. `FeedEventsController#create` resolves the current user from the session; if no user is identified the action responds `200 OK` without writing anything.
3. `FeedEvents::BulkUpsert` validates each event using `FeedEvent` model validations, discarding those with missing article ids, invalid categories, negative positions, or unrecognised context types.
4. Within the surviving events, any pair sharing the same user, article, and category that was also seen in the database within the timebox is suppressed.
5. The remaining events are inserted in bulk; article counters are then updated for a sampled subset (up to 5) of the affected article ids.

### System recomputes article feed success score after save

1. After any `FeedEvent` is saved, `update_article_counters_and_scores` is triggered.
2. For the event's article, the system counts distinct users per category and computes a weighted score: `(clicks + pageviews + reactions * 6 + comments * 12) / distinct_impression_users`.
3. The article's `feed_success_score`, `feed_impressions_count`, and `feed_clicks_count` columns are updated atomically. The call is throttled so recalculation occurs at most once every 5 minutes per article.

### System branches feed configuration on high-value engagement

1. When a `FeedEvent` with category `reaction` or `comment` is saved and a `feed_config` is associated, `create_feed_config_offshoot` fires.
2. The current `FeedConfig` creates a slightly modified evolutionary clone of itself, allowing the feed algorithm to explore variants informed by the engagement signal.

## Failures / Exceptions

- Events submitted without a valid authenticated session are silently ignored; the endpoint always returns `200 OK` to avoid leaking information.
- Invalid enum values for `category` raise `ArgumentError` inside `BulkUpsert#valid_events`; these are rescued and the offending event is dropped rather than aborting the entire batch.
- If the entire batch contains no valid events after filtering, `BulkUpsert#call` returns early without issuing any database queries.
- `FeedTracker` constructor logs a console error and returns without initialising if `feedItemsRoot` or `config` are missing.
- `sendBeacon` failure causes `beaconEnabled` to be set to `false` for the remainder of the session; subsequent batches use the `fallbackRequest` fetch path with `keepalive: true`.
