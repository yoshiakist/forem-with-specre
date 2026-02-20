---
id: "01KHY7Q0D5F8MAW2DBGCNMX00R"
name: "podcasts_podcast_create_api"
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
- spec/requests/podcasts/podcast_create_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Podcast` within the podcasts domain.

### Behavioral Areas

- **Podcast Create**: creates a podcast with valid attributes
- **when unauthorized user**: creates a podcast_admin role when created by an owner
- **when signed in**: creates a podcast_admin role when created by an owner

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

### S-1: redirects

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects

### S-2: renders new

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders new

### S-3: creates a podcast with valid attributes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a podcast with valid attributes

### S-4: creates an unpublished podcast

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an unpublished podcast

### S-5: creates a podcast with correct attributes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a podcast with correct attributes

### S-6: creates a podcast_admin role when created by an owner

- **Given** the system is in a standard operational state
- **When** created by an owner
- **Then** creates a podcast_admin role

### S-7: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-8: sets the creator

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the creator

### S-9: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-10: returns error if image file name is too long

- **Given** image file name is too long
- **When** the action is triggered
- **Then** returns error

### S-11: returns error if image is not a file

- **Given** image is not a file
- **When** the action is triggered
- **Then** returns error

### S-12: returns error if pattern_image file name is too long

- **Given** pattern_image file name is too long
- **When** the action is triggered
- **Then** returns error

