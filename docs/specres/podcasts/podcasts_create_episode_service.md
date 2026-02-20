---
id: "01KHY7Q0DQERWVZ0925R33BY9H"
name: "podcasts_create_episode_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/podcasts/create_episode.rb
- app/controllers/admin/podcasts_controller.rb
- app/controllers/podcasts_controller.rb
- app/services/podcasts/episode_rss_item.rb
- app/services/podcasts/feed.rb
- app/services/podcasts/get_episode.rb
- app/services/podcasts/get_media_url.rb
- app/services/podcasts/update_episode_media_url.rb
- app/services/users/delete_podcasts.rb
- app/workers/podcasts/bust_cache_worker.rb
- app/workers/podcasts/enqueue_get_episodes_worker.rb
- spec/services/podcasts/create_episode_spec.rb

## Functional Overview

This specification defines the expected behavior of `Podcasts::CreateEpisode` within the podcasts domain.

### Behavioral Areas

- **when item has an https media_url**: rescues an exception when pubDate is invalid
- **when item has an http media url**: rescues an exception when pubDate is invalid
- **when item is not a podcast episode**: creates an episode
- **when attempting to create duplicate episodes**: creates an episode
- **when episodes contain non-latin script titles**: rescues an exception when pubDate is invalid

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/podcasts/create_episode.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/admin/podcasts_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/podcasts_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/podcasts/episode_rss_item.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/feed.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/get_episode.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/get_media_url.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/podcasts/update_episode_media_url.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/delete_podcasts.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/podcasts/bust_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/podcasts/enqueue_get_episodes_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: creates an episode

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an episode

### S-2: creates an episode with correct data

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an episode with correct data

### S-3: populates processed_html

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** populates processed_html

### S-4: sets correct availability statuses

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets correct availability statuses

### S-5: rescues an exception when pubDate is invalid

- **Given** the system is in a standard operational state
- **When** pubDate is invalid
- **Then** rescues an exception

### S-6: rescues an exception when pubDate is nil

- **Given** the system is in a standard operational state
- **When** pubDate is nil
- **Then** rescues an exception

### S-7: sets media_url to https version when it is available

- **Given** the system is in a standard operational state
- **When** it is available
- **Then** sets media_url to https version

### S-8: keeps an http media url when https version is not available

- **Given** the system is in a standard operational state
- **When** https version is not available
- **Then** keeps an http media url

### S-9: does not raise error

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not raise error

### S-10: does not create episode

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create episode

### S-11: updates existing episode

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates existing episode

### S-12: updates columns

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates columns

