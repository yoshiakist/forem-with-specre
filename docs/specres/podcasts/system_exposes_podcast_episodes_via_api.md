---
id: "01KHZ7J1AT0XZH85CCGJ8MKN03"
name: "system_exposes_podcast_episodes_via_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/concerns/api/podcast_episodes_controller.rb`
- `app/controllers/api/v0/podcast_episodes_controller.rb`
- `app/controllers/api/v1/podcast_episodes_controller.rb`
- `app/views/api/v0/podcast_episodes/index.json.jbuilder` (Template)
- `app/views/api/v1/podcast_episodes/index.json.jbuilder` (Template)
- `spec/requests/api/v0/podcasts_episodes_spec.rb` (Test)
- `spec/requests/api/v1/podcasts_episodes_spec.rb` (Test)
- `spec/requests/api/v1/docs/podcast_episodes_spec.rb` (Test)

## Functional Overview

The system exposes a paginated `GET /api/podcast_episodes` endpoint available in both API v0 and v1. It returns a JSON array of reachable podcast episodes belonging to published podcasts, ordered by descending publication date. The response for each episode includes its id, path, title, image URL (falling back to the podcast's image), and a nested podcast object with title, slug, and image URL. Results can be filtered to a specific podcast by supplying a `username` query parameter matching the podcast's slug. Pagination is controlled via `page` and `per_page` parameters, with `per_page` capped by the `API_PER_PAGE_MAX` application configuration value (default 1000). Both versions share implementation through the `Api::PodcastEpisodesController` concern and set edge-caching surrogate key headers on responses.

## Scenarios

### Listing all reachable podcast episodes

1. A client sends `GET /api/podcast_episodes`.
2. The system queries all `PodcastEpisode` records that are reachable and belong to published (available) podcasts, joined with their podcasts.
3. Results are ordered by descending `published_at` date.
4. The system returns a JSON array where each element contains `type_of`, `class_name`, `id`, `path`, `title`, `image_url`, and a nested `podcast` object with `title`, `slug`, and `image_url`.

### Filtering episodes by podcast username

1. A client sends `GET /api/podcast_episodes?username=<slug>`.
2. The system looks up the podcast whose slug matches the given username; the podcast must be published and available.
3. If no matching available podcast exists, the system responds with HTTP 404.
4. If found, only episodes belonging to that podcast that are reachable are included in the response.

### Paginating results

1. A client sends `GET /api/podcast_episodes` with `page` and `per_page` query parameters.
2. The system resolves the effective page size as the minimum of the requested `per_page` and `API_PER_PAGE_MAX` (defaulting to 30 per page, max 1000).
3. The system returns the requested page slice of the ordered result set.

### Edge-caching surrogate keys

1. On each successful response, the system sets a `surrogate-key` response header.
2. The header contains the table-level key `podcast_episodes` and the record-level key for each episode included in the response.
3. This enables CDN-level cache invalidation at both the collection and individual episode granularity.

## Failures / Exceptions

- When the `username` parameter is provided and no available (published) podcast with that slug exists, the system responds with HTTP 404 (raised via `find_by!`).
- Unreachable podcast episodes are excluded from all responses regardless of other filters.
- Episodes belonging to unpublished podcasts are excluded from the global listing, and requesting them by `username` results in a 404.
