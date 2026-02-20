---
id: "01KHY7Q0DD159EVR5JADJ0DRZR"
name: "podcasts_podcast_show_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/podcasts_controller.rb
- app/controllers/podcasts_controller.rb
- app/services/podcasts/create_episode.rb
- app/services/podcasts/episode_rss_item.rb
- app/services/podcasts/feed.rb
- app/services/podcasts/get_episode.rb
- app/services/podcasts/get_media_url.rb
- app/services/podcasts/update_episode_media_url.rb
- app/services/users/delete_podcasts.rb
- app/workers/podcasts/bust_cache_worker.rb
- spec/requests/podcasts/podcast_show_spec.rb

## Functional Overview

This specification defines the expected behavior of `"PodcastShow"` within the podcasts domain.

### Behavioral Areas

- **PodcastShow**: Ensures correct behavior under the specified conditions
- **GET podcast show**: renders 404 for an unreachable podcast

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/podcasts_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/podcasts_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/podcasts/create_episode.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/episode_rss_item.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/feed.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/get_episode.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/get_media_url.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/update_episode_media_url.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/delete_podcasts.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/podcasts/bust_cache_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: renders 404 for an unreachable podcast

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders 404 for an unreachable podcast

### S-2: renders ok

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders ok

### S-3: shows reachable podcasts

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows reachable podcasts

### S-4: renders 404 when podcast is unpublished

- **Given** the system is in a standard operational state
- **When** podcast is unpublished
- **Then** renders 404

