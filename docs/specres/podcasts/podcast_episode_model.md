---
id: "01KHY7Q0CRVVVDKPBRPN7SP3G3"
name: "podcast_episode_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/api/v0/podcast_episodes_controller.rb
- app/controllers/api/v1/podcast_episodes_controller.rb
- app/controllers/concerns/api/podcast_episodes_controller.rb
- app/controllers/podcast_episodes_controller.rb
- app/decorators/podcast_episode_decorator.rb
- app/models/concerns/algolia_searchable/searchable_podcast_episode.rb
- app/models/podcast_episode.rb
- app/models/podcast_episode_appearance.rb
- app/serializers/search/podcast_episode_serializer.rb
- app/services/edge_cache/bust_podcast_episode.rb
- app/services/search/podcast_episode.rb
- app/models/podcast.rb
- app/models/podcast_ownership.rb
- spec/models/podcast_episode_spec.rb

## Functional Overview

This specification defines the expected behavior of `PodcastEpisode` within the podcasts domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions
- **search_id**: Ensures correct behavior under the specified conditions
- **description**: Ensures correct behavior under the specified conditions
- **.available**: Ensures correct behavior under the specified conditions
- **when callbacks are triggered before validation**: is available when reachable and published
- **paragraphs cleanup**: removes empty paragraphs
- **Cloudinary configuration and processing**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/api/v0/podcast_episodes_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/podcast_episodes_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/podcast_episodes_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/podcast_episodes_controller.rb` -- HTTP request routing and response handling
- **Decorator**: `app/decorators/podcast_episode_decorator.rb` -- presentation logic and view-model enrichment
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_podcast_episode.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/podcast_episode.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/podcast_episode_appearance.rb` -- data persistence, validations, and associations
- **Serializer**: `app/serializers/search/podcast_episode_serializer.rb` -- API response formatting and data transformation
- **Service layer**: `app/services/edge_cache/bust_podcast_episode.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/search/podcast_episode.rb` -- business logic orchestration and domain operations
- **Model layer**: `app/models/podcast.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to podcast
- have many comments.inverse of commentable.dependent nullify
- have many podcast episode appearances.dependent destroy
- have many users.through podcast episode appearances
- validate presence of comments count
- validate presence of guid
- validate presence of media url
- validate presence of reactions count
- validate presence of slug
- validate presence of title

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: validates guid uniqueness

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates guid uniqueness

### S-3: validates media_url uniqueness

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates media_url uniqueness

### S-4: returns podcast_episode_ID

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns podcast_episode_ID

### S-5: strips tags from the body

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** strips tags from the body

### S-6: is available when reachable and published

- **Given** the system is in a standard operational state
- **When** reachable and published
- **Then** is available

### S-7: is not available when unreachable

- **Given** the system is in a standard operational state
- **When** unreachable
- **Then** is not available

### S-8: is not available when podcast is unpublished

- **Given** the system is in a standard operational state
- **When** podcast is unpublished
- **Then** is not available

### S-9: removes empty paragraphs

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes empty paragraphs

### S-10: adds a wrapping paragraph

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds a wrapping paragraph

### S-11: does not add a wrapping paragraph if already present

- **Given** already present
- **When** the action is triggered
- **Then** does not add a wrapping paragraph

### S-12: prefixes an image URL with a path

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** prefixes an image URL with a path

### S-13: chooses the appropriate quality for an image

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** chooses the appropriate quality for an image

