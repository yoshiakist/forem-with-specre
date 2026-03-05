---
id: "01KHZ27T6PAPJ71DGHEYS3B02Y"
name: "user_can_search_podcast_episodes"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/search_controller.rb`
- `app/services/search/podcast_episode.rb`
- `app/serializers/search/podcast_episode_serializer.rb`
- `spec/services/search/podcast_episode_spec.rb` (Test)
- `spec/serializers/search/podcast_episode_serializer_spec.rb` (Test)

## Functional Overview

Users can search for podcast episodes on the platform by selecting the "Podcasts" content type filter on the search results page. The podcast episode search uses PostgreSQL full-text search against episode body, title, and subtitle. Only episodes from published podcasts that are marked as reachable are included. Results display episode metadata including title, summary, path, publication date, and associated podcast information (name and image).

## Scenarios

### User searches podcast episodes by keyword

1. User enters a search query and selects the podcast episode content type filter
2. `SearchController#feed_content` delegates to `Search::PodcastEpisode.search_documents` with the query term
3. Service queries reachable episodes from published podcasts, applying full-text search via `.search_podcast_episodes(term)`
4. Results include episode title, summary, body text, path, publication date, reaction counts, and nested podcast metadata (name, slug, image)

### User sorts podcast episode results by date

1. User selects a sort option (Newest or Oldest) while viewing podcast results
2. Service applies `published_at` ordering in the requested direction
3. When no explicit sort is provided, no specific ordering is applied (database default order)

### System excludes episodes from unpublished or unreachable podcasts

1. A podcast episode search query is executed
2. The service only includes episodes where the parent podcast is published
3. Episodes marked as unreachable are excluded from results
