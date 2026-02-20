---
id: "01KHY7Q0DWZPEYQJC01TVYWXH8"
name: "podcasts_feed_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/podcasts/feed.rb
- app/controllers/admin/podcasts_controller.rb
- app/controllers/podcasts_controller.rb
- app/services/podcasts/create_episode.rb
- app/services/podcasts/episode_rss_item.rb
- app/services/podcasts/get_episode.rb
- app/services/podcasts/get_media_url.rb
- app/services/podcasts/update_episode_media_url.rb
- app/services/users/delete_podcasts.rb
- app/workers/podcasts/bust_cache_worker.rb
- app/workers/podcasts/enqueue_get_episodes_worker.rb
- spec/services/podcasts/feed_spec.rb

## Functional Overview

This specification defines the expected behavior of `Podcasts::Feed` within the podcasts domain.

### Behavioral Areas

- **when unreachable**: sets reachable when hitting ip issue
- **when ssl certificate is not valid**: sets reachable when hitting ip issue
- **when creating**: sets reachable when hitting ip issue
- **when updating**: sets reachable when hitting ip issue

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/podcasts/feed.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/admin/podcasts_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/podcasts_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/podcasts/create_episode.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/episode_rss_item.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/get_episode.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/get_media_url.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/update_episode_media_url.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/delete_podcasts.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/podcasts/bust_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/podcasts/enqueue_get_episodes_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: sets reachable and status

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets reachable and status

### S-2: sets reachable

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets reachable

### S-3: sets reachable when hitting ip issue

- **Given** the system is in a standard operational state
- **When** hitting ip issue
- **Then** sets reachable

### S-4: sets reachable when there redirection is too deep

- **Given** the system is in a standard operational state
- **When** there redirection is too deep
- **Then** sets reachable

### S-5: schedules the update url jobs when setting as unreachable

- **Given** the system is in a standard operational state
- **When** setting as unreachable
- **Then** schedules the update url jobs

### S-6: re-checks episodes urls when setting as unreachable

- **Given** the system is in a standard operational state
- **When** setting as unreachable
- **Then** re-checks episodes urls

### S-7: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-8: sets ssl_failed

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets ssl_failed

### S-9: fetches podcast episodes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** fetches podcast episodes

### S-10: fetches correct podcasts

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** fetches correct podcasts

### S-11: does not refetch already fetched episodes

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not refetch already fetched episodes

### S-12: updates published_at for existing episodes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates published_at for existing episodes

