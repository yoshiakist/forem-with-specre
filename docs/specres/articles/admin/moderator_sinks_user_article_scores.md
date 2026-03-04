---
id: "01KJV8A14A58JBDS2RRK1MY5YH"
name: "moderator_sinks_user_article_scores"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/services/moderator/sink_articles.rb`
- `app/workers/moderator/sink_articles_worker.rb`
- `spec/services/moderator/sink_articles_spec.rb` (Test)
- `spec/workers/moderator/sink_articles_worker_spec.rb` (Test)

## Functional Overview

When a moderator flags a user (typically via a vomit reaction), the system enqueues a background job that recalculates and lowers the score of every published article belonging to that user. The service entry point (`Moderator::SinkArticles`) is a thin dispatcher that immediately hands off work to an async Sidekiq job (`Moderator::SinkArticlesWorker`). The worker fetches the user, iterates over all their published subforem articles, and calls `update_score` on each one, which internally invokes the hotness-score algorithm. The degree of score reduction depends on whether the moderator reaction has been confirmed. If the user cannot be found, the job exits silently. Errors during processing are reported to ForemStatsClient and Honeybadger without re-raising.

## Scenarios

### Moderator initiates a sink for a flagged user

1. A moderator triggers `Moderator::SinkArticles.call(user_id)`.
2. The service enqueues `Moderator::SinkArticlesWorker` on the `medium_priority` queue with the given user ID.
3. The job is picked up asynchronously with up to 10 retries configured.

### Worker recalculates scores for all published articles

1. The worker receives the user ID and looks up the user.
2. It queries all published, subforem-scoped articles belonging to that user.
3. For each article, it calls `update_score`, which recomputes the hotness score (via `BlackBox.article_hotness_score`), effectively sinking it relative to clean users.

### Score reduction reflects unconfirmed vomit reaction

1. A user has articles with a baseline score of 0.
2. A moderator places an unconfirmed vomit reaction on the user.
3. After the sink job runs, each article's score drops by approximately 25 points (exact values depend on publication timing).

### Score reduction reflects confirmed vomit reaction

1. A user has articles with a baseline score of 0.
2. A moderator's vomit reaction on the user is confirmed.
3. After the sink job runs, each article's score drops by approximately 50 points — double the unconfirmed penalty.

### Worker skips when user is not found

1. The worker is called with a user ID that does not correspond to any existing user.
2. The worker returns immediately without processing any articles and without raising an error.

### Worker skips draft (unpublished) articles

1. A user has unpublished (draft) articles.
2. The sink job runs for that user.
3. Draft articles are excluded from score recalculation; only published articles are affected.

## Failures / Exceptions

- If a `StandardError` is raised during article score updates, the worker increments a `moderators.sink` counter in ForemStatsClient (tagged `action:failed` and the user ID), notifies Honeybadger, and allows Sidekiq's retry mechanism to handle re-execution (up to 10 retries).
- If the user cannot be found by ID, the worker returns `nil` silently with no error raised or metric emitted.
