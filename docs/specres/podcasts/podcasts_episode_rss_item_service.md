---
id: "01KHY7Q0DSFBJAPJ6FEFKQD40T"
name: "podcasts_episode_rss_item_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/podcasts/episode_rss_item.rb
- app/controllers/admin/podcasts_controller.rb
- app/controllers/podcasts_controller.rb
- app/services/podcasts/create_episode.rb
- app/services/podcasts/feed.rb
- app/services/podcasts/get_episode.rb
- app/services/podcasts/get_media_url.rb
- app/services/podcasts/update_episode_media_url.rb
- app/services/users/delete_podcasts.rb
- app/workers/podcasts/bust_cache_worker.rb
- app/workers/podcasts/enqueue_get_episodes_worker.rb
- spec/services/podcasts/episode_rss_item_spec.rb

## Functional Overview

This specification defines the expected behavior of `Podcasts::EpisodeRssItem` within the podcasts domain.

### Behavioral Areas

- **new**: Ensures correct behavior under the specified conditions
- **from_item**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/podcasts/episode_rss_item.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/admin/podcasts_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/podcasts_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/podcasts/create_episode.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/feed.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/get_episode.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/get_media_url.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/update_episode_media_url.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/delete_podcasts.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/podcasts/bust_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/podcasts/enqueue_get_episodes_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: create a nice object

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** create a nice object

### S-2: returns a hash

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a hash

### S-3: has attr readers

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** has attr readers

### S-4: sets url to nil when no enclosure

- **Given** the system is in a standard operational state
- **When** no enclosure
- **Then** sets url to nil

