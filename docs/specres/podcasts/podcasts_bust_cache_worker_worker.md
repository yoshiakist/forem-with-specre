---
id: "01KHY7Q0EMX31MQJF04AWA1Q2M"
name: "podcasts_bust_cache_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/podcast_episodes/bust_cache_worker.rb
- app/workers/podcasts/bust_cache_worker.rb
- app/controllers/admin/podcasts_controller.rb
- app/controllers/podcasts_controller.rb
- app/services/podcasts/create_episode.rb
- app/services/podcasts/episode_rss_item.rb
- app/services/podcasts/feed.rb
- app/services/podcasts/get_episode.rb
- app/services/podcasts/get_media_url.rb
- app/services/podcasts/update_episode_media_url.rb
- app/services/users/delete_podcasts.rb
- app/workers/podcasts/enqueue_get_episodes_worker.rb
- spec/workers/podcasts/bust_cache_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Podcasts::BustCacheWorker` within the podcasts domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/podcast_episodes/bust_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/podcasts/bust_cache_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/podcasts_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/podcasts_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/podcasts/create_episode.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/episode_rss_item.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/feed.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/get_episode.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/get_media_url.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/update_episode_media_url.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/delete_podcasts.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/podcasts/enqueue_get_episodes_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: busts cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts cache

