---
id: "01KHY7Q0EJQBFH1BQR7ZTZFD22"
name: "podcast_episodes_update_media_url_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/podcast_episodes/update_media_url_worker.rb
- app/controllers/api/v0/podcast_episodes_controller.rb
- app/controllers/api/v1/podcast_episodes_controller.rb
- app/controllers/concerns/api/podcast_episodes_controller.rb
- app/controllers/podcast_episodes_controller.rb
- app/workers/podcast_episodes/bust_cache_worker.rb
- app/workers/podcast_episodes/create_worker.rb
- spec/workers/podcast_episodes/update_media_url_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `PodcastEpisodes::UpdateMediaUrlWorker` within the podcasts domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/podcast_episodes/update_media_url_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/api/v0/podcast_episodes_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/podcast_episodes_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/podcast_episodes_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/podcast_episodes_controller.rb` -- HTTP request routing and response handling
- **Background worker**: `app/workers/podcast_episodes/bust_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/podcast_episodes/create_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: calls the service

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls the service

### S-2: raises an error if episode is not found

- **Given** episode is not found
- **When** the action is triggered
- **Then** raises an error

