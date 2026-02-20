---
id: "01KHY7Q0D7TVS7TVH2306EEYS3"
name: "podcasts_podcast_episodes_index_api"
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
- spec/requests/podcasts/podcast_episodes_index_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Podcast` within the podcasts domain.

### Behavioral Areas

- **Podcast Episodes Index Spec**: shows reachable podcasts
- **GET podcast episodes index**: shows reachable podcasts

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

### S-1: renders page with proper sidebar

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders page with proper sidebar

### S-2: shows reachable podcasts

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows reachable podcasts

### S-3: shows featured podcasts area if there are any

- **Given** there are any
- **When** the action is triggered
- **Then** shows featured podcasts area

### S-4: does not show featured podcasts area if there are not any

- **Given** there are not any
- **When** the action is triggered
- **Then** does not show featured podcasts area

### S-5: sets proper surrogate key

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets proper surrogate key

### S-6: redirects /podcasts to /pod

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects /podcasts to /pod

