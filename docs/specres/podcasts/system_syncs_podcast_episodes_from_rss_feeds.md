---
id: "01KHZ7C8VY10XGW8GDHDDHSHRQ"
name: "system_syncs_podcast_episodes_from_rss_feeds"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/services/podcasts/feed.rb`
- `app/services/podcasts/get_episode.rb`
- `app/services/podcasts/create_episode.rb`
- `app/services/podcasts/episode_rss_item.rb`
- `app/services/podcasts/get_media_url.rb`
- `app/services/podcasts/update_episode_media_url.rb`
- `app/models/podcast_episode.rb`
- `app/workers/podcasts/enqueue_get_episodes_worker.rb`
- `app/workers/podcasts/get_episodes_worker.rb`
- `app/workers/podcast_episodes/create_worker.rb`
- `app/workers/podcast_episodes/update_media_url_worker.rb`
- `spec/services/podcasts/feed_spec.rb` (Test)
- `spec/services/podcasts/get_episode_spec.rb` (Test)
- `spec/services/podcasts/create_episode_spec.rb` (Test)
- `spec/services/podcasts/episode_rss_item_spec.rb` (Test)
- `spec/services/podcasts/get_media_url_spec.rb` (Test)
- `spec/services/podcasts/update_episode_media_url_spec.rb` (Test)
- `spec/models/podcast_episode_spec.rb` (Test)
- `spec/workers/podcasts/enqueue_get_episodes_worker_spec.rb` (Test)
- `spec/workers/podcasts/get_episodes_worker_spec.rb` (Test)
- `spec/workers/podcast_episodes/create_worker_spec.rb` (Test)
- `spec/workers/podcast_episodes/update_media_url_worker_spec.rb` (Test)

## Functional Overview

The system periodically fetches RSS feeds for all published podcasts and synchronizes their episodes into the database. A scheduled worker (`Podcasts::EnqueueGetEpisodesWorker`) enqueues per-podcast jobs (`Podcasts::GetEpisodesWorker`), each of which fetches the RSS feed via `Podcasts::Feed`, parses items using `Podcasts::EpisodeRssItem`, and delegates per-item processing to `Podcasts::GetEpisode`. New episodes are cached and created asynchronously via `PodcastEpisodes::CreateWorker`, which invokes `Podcasts::CreateEpisode` to resolve the media URL's reachability and HTTPS availability through `Podcasts::GetMediaUrl` before upserting the `PodcastEpisode` record. Existing episodes whose media URLs are stale, unreachable, or non-HTTPS are updated asynchronously via `PodcastEpisodes::UpdateMediaUrlWorker` and `Podcasts::UpdateEpisodeMediaUrl`. When a feed itself becomes unreachable, the podcast is marked accordingly and all of its episode media URLs are re-verified to determine whether the episodes should remain visible.

## Design Intent

Episode data is stored in Rails cache before async creation to decouple RSS parsing from database writes and to keep the feed-fetching worker lightweight. `PodcastEpisode.upsert` is used instead of `find_or_create_by` to avoid race conditions and to support bulk imports, at the cost of not running ActiveRecord callbacks on create. The system prefers HTTPS media URLs and silently upgrades HTTP URLs when an HTTPS counterpart is reachable, falling back to HTTP only when HTTPS is unavailable.

## Key Members

- `Podcasts::Feed#get_episodes(limit:, force_update:)` — top-level entry point; fetches and parses the RSS feed, sorts items by publish date descending, and processes up to `limit` items
- `Podcasts::EpisodeRssItem` — serializable value object wrapping an RSS item; used as the cache-safe transfer format between workers
- `Podcasts::GetMediaUrl` — resolves whether a media URL is reachable and whether HTTPS is available; returns a struct with `https`, `reachable`, and `url` fields
- `PodcastEpisode` — the persisted episode model; validates uniqueness of `guid` and `media_url`; exposes `reachable` and `https` boolean columns

## Scenarios

### Scheduled sync enqueues per-podcast jobs

1. `Podcasts::EnqueueGetEpisodesWorker` runs on a schedule and queries all published podcast IDs.
2. It bulk-enqueues one `Podcasts::GetEpisodesWorker` job per podcast, passing a limit of 5 episodes.
3. Each `Podcasts::GetEpisodesWorker` job looks up the podcast and calls `Podcasts::Feed#get_episodes`.

### Feed fetched and new episodes created

1. `Podcasts::Feed` fetches the RSS feed URL via HTTP with a redirect limit of 7.
2. The feed items are sorted by `pubDate` descending and the first `limit` items are processed.
3. For each item, `Podcasts::GetEpisode` wraps the raw RSS item in a `Podcasts::EpisodeRssItem`.
4. If the item has no enclosure URL, processing is skipped.
5. If no matching episode exists, the item data is written to the Rails cache and `PodcastEpisodes::CreateWorker` is enqueued.
6. `PodcastEpisodes::CreateWorker` reads the cached item and calls `Podcasts::CreateEpisode`, which resolves the media URL and upserts the `PodcastEpisode` record.
7. After all items are processed, the podcast is marked `reachable: true` with a cleared status notice.

### Existing episode with stale or non-HTTPS media URL is updated

1. When `Podcasts::GetEpisode` finds a matching episode that is unreachable or served over HTTP, and the episode was created within the last 12 hours (or `force_update` is true), it enqueues `PodcastEpisodes::UpdateMediaUrlWorker`.
2. The worker calls `Podcasts::UpdateEpisodeMediaUrl`, which re-runs `Podcasts::GetMediaUrl` against the enclosure URL.
3. The episode's `media_url`, `reachable`, and `https` fields are updated and saved.

### Media URL resolved with HTTPS preference

1. `Podcasts::GetMediaUrl` receives an enclosure URL (HTTP or HTTPS).
2. It always attempts the HTTPS variant first by substituting the scheme.
3. If the HTTPS HEAD request returns HTTP 200, the episode is stored with the HTTPS URL and marked `https: true, reachable: true`.
4. If HTTPS is unreachable and the original URL was HTTP, the HTTP URL is checked; if reachable, the episode is stored with `https: false, reachable: true`.
5. If both are unreachable, the episode is stored with `reachable: false`.

### Feed becomes unreachable and episodes are re-verified

1. If fetching the RSS feed raises a network error (timeout, connection refused, SSL failure, or too many redirects), `Podcasts::Feed` marks the podcast `reachable: false` and sets a localized `status_notice`.
2. If the podcast was previously reachable (or `force_update` is true), it bulk-enqueues `PodcastEpisodes::UpdateMediaUrlWorker` for all episodes to re-verify their media URLs.
3. If the podcast was already unreachable, no re-verification jobs are scheduled.

## Failures / Exceptions

- `Net::OpenTimeout`, `Errno::ECONNREFUSED`, `Errno::EHOSTUNREACH`, `SocketError`, `HTTParty::RedirectionTooDeep` during feed fetch: podcast marked `unreachable` with status `:unreachable`.
- `OpenSSL::SSL::SSLError` during feed fetch: podcast marked `unreachable` with status `:ssl_failed`.
- `RSS::NotWellFormedError` or unparsable response body: podcast marked `unreachable` with status `:unparsable`.
- Invalid or nil `pubDate` on an RSS item: `ArgumentError` / `NoMethodError` is rescued and `published_at` is left nil; episode creation continues.
- Missing enclosure URL on an RSS item: episode is skipped entirely without enqueuing any worker.
- `PodcastEpisodes::UpdateMediaUrlWorker` raises `ActiveRecord::RecordNotFound` when the episode does not exist.
