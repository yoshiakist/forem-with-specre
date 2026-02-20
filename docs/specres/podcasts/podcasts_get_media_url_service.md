---
id: "01KHY7Q0E1VAWYE101FW419A6G"
name: "podcasts_get_media_url_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/podcasts/get_media_url.rb
- app/controllers/admin/podcasts_controller.rb
- app/controllers/podcasts_controller.rb
- app/services/podcasts/create_episode.rb
- app/services/podcasts/episode_rss_item.rb
- app/services/podcasts/feed.rb
- app/services/podcasts/get_episode.rb
- app/services/podcasts/update_episode_media_url.rb
- app/services/users/delete_podcasts.rb
- app/workers/podcasts/bust_cache_worker.rb
- app/workers/podcasts/enqueue_get_episodes_worker.rb
- spec/services/podcasts/get_media_url_spec.rb

## Functional Overview

This specification defines the expected behavior of `Podcasts::GetMediaUrl` within the podcasts domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/podcasts/get_media_url.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/admin/podcasts_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/podcasts_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/podcasts/create_episode.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/episode_rss_item.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/feed.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/get_episode.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/update_episode_media_url.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/delete_podcasts.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/podcasts/bust_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/podcasts/enqueue_get_episodes_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: https, reachable

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** https, reachable

### S-2: normalizes url

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** normalizes url

### S-3: https, unreachable

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** https, unreachable

### S-4: http, https reachable

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** http, https reachable

### S-5: http, https unreachable, http reachable

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** http, https unreachable, http reachable

### S-6: http, https unreachable

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** http, https unreachable

### S-7: http, https unreachable with other exception

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** http, https unreachable with other exception

### S-8: http, https unreachable with invalid url exception

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** http, https unreachable with invalid url exception

### S-9: http, https unreachable with openssl error

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** http, https unreachable with openssl error

### S-10: marks unreachable with addressable invalid url exception

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** marks unreachable with addressable invalid url exception

### S-11: marks socket errors as invalid url exception

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** marks socket errors as invalid url exception

