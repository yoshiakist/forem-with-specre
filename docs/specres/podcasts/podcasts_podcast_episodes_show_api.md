---
id: "01KHY7Q0DA9GMJT47X557AXE40"
name: "podcasts_podcast_episodes_show_api"
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
- spec/requests/podcasts/podcast_episodes_show_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Podcast` within the podcasts domain.

### Behavioral Areas

- **Podcast Episodes Show Spec**: renders the correct podcast episode
- **GET podcast episodes show**: renders the correct podcast episode
- **with comments**: displays only good standing comments for signed out

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

### S-1: renders the correct podcast episode

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the correct podcast episode

### S-2: does not render another podcast

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not render another podcast

### S-3: displays only good standing comments for signed out

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays only good standing comments for signed out

### S-4: displays all comments above > -400 for signed in

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays all comments above > -400 for signed in

### S-5: displays deleted message and children of a spam comment for signed in

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays deleted message and children of a spam comment for signed in

### S-6: displays a low-quality marker for a low-quality comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays a low-quality marker for a low-quality comment

