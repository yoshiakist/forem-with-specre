---
id: "01KHZ7FNBPTBWCMXWYERHJHSS0"
name: "system_busts_podcast_caches_on_content_change"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/services/edge_cache/bust_podcast.rb`
- `app/services/edge_cache/bust_podcast_episode.rb`
- `app/workers/podcasts/bust_cache_worker.rb`
- `app/workers/podcast_episodes/bust_cache_worker.rb`
- `spec/services/edge_cache/bust_podcast_spec.rb` (Test)
- `spec/services/edge_cache/bust_podcast_episode_spec.rb` (Test)
- `spec/workers/podcasts/bust_cache_worker_spec.rb` (Test)
- `spec/workers/podcast_episodes/bust_cache_worker_spec.rb` (Test)

## Functional Overview

When podcast or podcast episode content changes, the system invalidates the relevant edge-cache entries to ensure users receive up-to-date content. Two lightweight service objects — `EdgeCache::BustPodcast` and `EdgeCache::BustPodcastEpisode` — encapsulate the cache-busting logic and are invoked asynchronously through their corresponding Sidekiq workers (`Podcasts::BustCacheWorker` and `PodcastEpisodes::BustCacheWorker`). The podcast service busts the podcast's own path, while the episode service additionally purges the episode record directly, invalidates the episode's path, the parent podcast's path, and the global `/pod` listing path, swallowing any errors from the CDN bust calls so that failures do not propagate to callers.

## Design Intent

The burst is split into two separate service/worker pairs — one for podcasts and one for podcast episodes — to keep each cache-clearing operation narrowly scoped. `BustPodcastEpisode` wraps CDN bust calls in a `rescue StandardError` block so that transient CDN failures are only logged (via `Rails.logger.warn`) rather than surfaced to the caller, preventing episode updates from failing solely due to cache-infrastructure issues.

## Scenarios

### Busting the cache for a podcast

1. A caller enqueues `Podcasts::BustCacheWorker` with the podcast's URL path.
2. The worker calls `EdgeCache::BustPodcast` with the path.
3. `EdgeCache::BustPodcast` verifies the path is present; if absent, it returns immediately without action.
4. When the path is present, the service constructs an `EdgeCache::Bust` instance and invokes it with the podcast's path (prefixed with `/`), invalidating that route at the CDN layer.

### Busting the cache for a podcast episode

1. A caller enqueues `PodcastEpisodes::BustCacheWorker` with the episode's ID, the episode's URL path, and the parent podcast's slug.
2. The worker returns immediately if either the path or slug is missing.
3. The worker looks up the `PodcastEpisode` record by ID; if no record is found, it returns without action.
4. With a valid episode, the worker delegates to `EdgeCache::BustPodcastEpisode`.
5. The service calls `purge` and `purge_all` on the episode record (model-level cache invalidation), then sends CDN bust requests for the episode's own path, the parent podcast's slug path, and the global `/pod` listing path.
6. If any CDN bust call raises a `StandardError`, the error is logged via `Rails.logger.warn` and the remaining work is abandoned gracefully.

### Skipping the bust when required data is absent

1. `EdgeCache::BustPodcast` is called with a `nil` path — it returns immediately without contacting the CDN.
2. `EdgeCache::BustPodcastEpisode` is called with any `nil` argument (episode, path, or slug) — it returns immediately without performing any purge or CDN call.
3. `PodcastEpisodes::BustCacheWorker` is performed with a `nil` path or `nil` slug — it returns before attempting a database lookup or calling the service.

## Failures / Exceptions

- If a `StandardError` is raised during any CDN bust call inside `EdgeCache::BustPodcastEpisode`, the error is caught and passed to `Rails.logger.warn`; no exception is re-raised to the worker or caller.
- If `PodcastEpisodes::BustCacheWorker` cannot find a `PodcastEpisode` record for the given ID, it returns without calling the service and without raising an error.
