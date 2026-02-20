---
id: "01KHY7Q0DJ43VT0MW5ZPB2SSAQ"
name: "edge_cache_bust_podcast_episode_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/edge_cache/bust_podcast_episode.rb
- app/services/edge_cache/bust_podcast.rb
- spec/services/edge_cache/bust_podcast_episode_spec.rb

## Functional Overview

This specification defines the expected behavior of `EdgeCache::BustPodcastEpisode` within the podcasts domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/edge_cache/bust_podcast_episode.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust_podcast.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: busts the cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts the cache

### S-2: logs an error

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs an error

