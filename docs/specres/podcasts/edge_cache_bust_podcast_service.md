---
id: "01KHY7Q0DMHD7Z5YZSWQKDQNZK"
name: "edge_cache_bust_podcast_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/edge_cache/bust_podcast.rb
- app/services/edge_cache/bust_podcast_episode.rb
- spec/services/edge_cache/bust_podcast_spec.rb

## Functional Overview

This specification defines the expected behavior of `EdgeCache::BustPodcast` within the podcasts domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/edge_cache/bust_podcast.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust_podcast_episode.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: busts the cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts the cache

