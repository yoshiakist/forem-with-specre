---
id: "01KJBWN5KRQKZE6SWZWPNHA43E"
name: "system_invalidates_article_edge_cache"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/services/edge_cache/bust_article.rb`
- `app/workers/articles/bust_cache_worker.rb`
- `app/workers/articles/bust_multiple_caches_worker.rb`
- `spec/services/edge_cache/bust_article_spec.rb` (Test)
- `spec/workers/articles/bust_cache_worker_spec.rb` (Test)
- `spec/workers/articles/bust_multiple_caches_worker_spec.rb` (Test)

## Functional Overview

When an article is published or updated, the system purges its CDN edge cache along with the caches of its author and organization. It then selectively invalidates home page and tag page routes based on the article's recency, score, and hotness: the home feed, top lists (week/month/year/infinity), the latest feed, video feed, and per-tag latest and top pages are all busted only when the article qualifies for each route. Two Sidekiq workers orchestrate this: `BustCacheWorker` handles a single article and delegates to `EdgeCache::BustArticle`, while `BustMultipleCachesWorker` handles a batch of article IDs and directly purges each article's canonical path and its `?i=i` variant.

## Design Intent

Cache busting is gated on qualification checks (score ranking, recency thresholds, hotness rank) rather than always flushing all routes. This avoids unnecessary cache churn for articles that would not appear in those listings, keeping CDN hit rates high while still ensuring freshness wherever the article is actually visible.

## Key Members

- `TIMEFRAMES` — Ordered list of `[timestamp_lambda, interval_name]` pairs covering week, month, year, and infinity windows; used to determine which `/top/:interval` routes need invalidation.

## Scenarios

### Single article cache bust via worker

1. A job is enqueued with an article ID.
2. `BustCacheWorker` looks up the article by ID.
3. If the article exists, it calls `EdgeCache::BustArticle` with the article record.
4. If the article does not exist, the worker exits silently without error.

### Full edge cache invalidation for an article

1. `EdgeCache::BustArticle` receives a published article.
2. The system purges the CDN representation of the article itself, its author, and (if present) its organization.
3. Home page busting is evaluated: if the article ranks in the top 4 by hotness score, `/` is invalidated; if it ranks in the top 3 for any TIMEFRAME window, the corresponding `/top/:interval` route is invalidated; if published within the last hour, `/latest` is invalidated; if it has a video and was published within 10 days, `/videos` is invalidated.
4. Tag page busting is evaluated for each tag: if published within the last 2 minutes, `/t/:tag/latest` is invalidated; if the article ranks in the top 3 for any TIMEFRAME within that tag, the corresponding `/top/:interval` and API pagination routes are invalidated; if it ranks in the top 2 by hotness for that tag (sampled with 50% probability), `/t/:tag` is invalidated.

### Batch cache bust for multiple articles

1. A job is enqueued with a list of article IDs.
2. `BustMultipleCachesWorker` fetches only the `id` and `path` columns for those articles.
3. For each article, it purges the article's canonical path and its `?i=i` variant, which forces CDN re-validation for both the HTML and inline-embed representations.

## Failures / Exceptions

- If `nil` is passed to `EdgeCache::BustArticle.call`, the method returns immediately without performing any cache operations.
- If `BustCacheWorker` cannot find an article by the given ID, it returns early without raising an error.
- `BustMultipleCachesWorker` uses `concurrency: { limit: 1 }` throttling and `retry: 10`, ensuring that burst invalidation jobs do not overwhelm the CDN purge API and will retry on transient failures.
