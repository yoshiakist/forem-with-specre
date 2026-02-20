---
id: "01KHY7Q0EDP5DJNSRDBHJSSYTT"
name: "podcast_episodes_bust_cache_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/podcast_episodes/bust_cache_worker.rb
- app/workers/podcasts/bust_cache_worker.rb
- app/controllers/api/v0/podcast_episodes_controller.rb
- app/controllers/api/v1/podcast_episodes_controller.rb
- app/controllers/concerns/api/podcast_episodes_controller.rb
- app/controllers/podcast_episodes_controller.rb
- app/workers/podcast_episodes/create_worker.rb
- app/workers/podcast_episodes/update_media_url_worker.rb
- spec/workers/podcast_episodes/bust_cache_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `PodcastEpisodes::BustCacheWorker` within the podcasts domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **when no podcast episode is found**: Ensures correct behavior under the specified conditions
- **when a path is not provided**: Ensures correct behavior under the specified conditions
- **when a slug is not provided**: Ensures correct behavior under the specified conditions
- **when podcast episode is found**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/podcast_episodes/bust_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/podcasts/bust_cache_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/api/v0/podcast_episodes_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/podcast_episodes_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/podcast_episodes_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/podcast_episodes_controller.rb` -- HTTP request routing and response handling
- **Background worker**: `app/workers/podcast_episodes/create_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/podcast_episodes/update_media_url_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: does not call the service

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call the service

### S-2: does not call the service

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call the service

### S-3: does not call the service

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call the service

### S-4: busts cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts cache

