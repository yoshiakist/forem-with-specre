---
id: "01KHY7Q0E4Q9X6GNF3N6DFSGGD"
name: "podcasts_update_episode_media_url_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/podcasts/update_episode_media_url.rb
- app/controllers/admin/podcasts_controller.rb
- app/controllers/podcasts_controller.rb
- app/services/podcasts/create_episode.rb
- app/services/podcasts/episode_rss_item.rb
- app/services/podcasts/feed.rb
- app/services/podcasts/get_episode.rb
- app/services/podcasts/get_media_url.rb
- app/services/users/delete_podcasts.rb
- app/workers/podcasts/bust_cache_worker.rb
- app/workers/podcasts/enqueue_get_episodes_worker.rb
- spec/services/podcasts/update_episode_media_url_spec.rb

## Functional Overview

This specification defines the expected behavior of `Podcasts::UpdateEpisodeMediaUrl` within the podcasts domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/podcasts/update_episode_media_url.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/admin/podcasts_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/podcasts_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/podcasts/create_episode.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/episode_rss_item.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/feed.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/get_episode.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/get_media_url.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/delete_podcasts.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/podcasts/bust_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/podcasts/enqueue_get_episodes_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: updates media_url from http to https

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates media_url from http to https

### S-2: keeps http when https and http are not reachable

- **Given** the system is in a standard operational state
- **When** https and http are not reachable
- **Then** keeps http

### S-3: does fine when there

- **Given** the system is in a standard operational state
- **When** there
- **Then** does fine

