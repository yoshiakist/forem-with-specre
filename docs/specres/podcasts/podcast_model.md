---
id: "01KHY7Q0CX423Z5QQA9WWTRH7H"
name: "podcast_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/podcasts_controller.rb
- app/controllers/api/v0/podcast_episodes_controller.rb
- app/controllers/api/v1/podcast_episodes_controller.rb
- app/controllers/concerns/api/podcast_episodes_controller.rb
- app/controllers/podcast_episodes_controller.rb
- app/controllers/podcasts_controller.rb
- app/decorators/podcast_episode_decorator.rb
- app/liquid_tags/podcast_tag.rb
- app/models/concerns/algolia_searchable/searchable_podcast_episode.rb
- app/models/podcast.rb
- app/models/podcast_episode.rb
- app/models/podcast_episode_appearance.rb
- app/models/podcast_ownership.rb
- app/serializers/search/podcast_episode_serializer.rb
- app/services/edge_cache/bust_podcast.rb
- spec/models/podcast_spec.rb

## Functional Overview

This specification defines the expected behavior of `Podcast` within the podcasts domain.

### Behavioral Areas

- **when callbacks are triggered after save**: triggers cache busting on save
- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions
- **.reachable**: Ensures correct behavior under the specified conditions
- **.available**: Ensures correct behavior under the specified conditions
- **existing_episode**: Ensures correct behavior under the specified conditions
- **admins**: returns podcast admins

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/podcasts_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/podcast_episodes_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/podcast_episodes_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/podcast_episodes_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/podcast_episodes_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/podcasts_controller.rb` -- HTTP request routing and response handling
- **Decorator**: `app/decorators/podcast_episode_decorator.rb` -- presentation logic and view-model enrichment
- **Liquid tag**: `app/liquid_tags/podcast_tag.rb` -- custom Markdown/Liquid embed rendering
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_podcast_episode.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/podcast.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/podcast_episode.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/podcast_episode_appearance.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to creator.class name "User".inverse of created podcasts.optional
- have many owners.through podcast ownerships
- have many podcast episodes.dependent destroy
- have many podcast ownerships.dependent destroy
- validate presence of feed url
- validate presence of image
- validate presence of main color hex
- validate presence of slug
- validate presence of title

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: has a creator

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** has a creator

### S-3: triggers cache busting on save

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** triggers cache busting on save

### S-4: validates slug uniqueness

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates slug uniqueness

### S-5: validates feed_url uniqueness

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates feed_url uniqueness

### S-6: validates feed_url format

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates feed_url format

### S-7: validates main_color_hex

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates main_color_hex

### S-8: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-9: is invalid when a user with a username equal to the podcast slug exists

- **Given** the system is in a standard operational state
- **When** a user with a username equal to the podcast slug exists
- **Then** is invalid

### S-10: is invalid when a page with a slug equal to the podcast slug exists

- **Given** the system is in a standard operational state
- **When** a page with a slug equal to the podcast slug exists
- **Then** is invalid

### S-11: is invalid when an org with a slug equal to the podcast slug exists

- **Given** the system is in a standard operational state
- **When** an org with a slug equal to the podcast slug exists
- **Then** is invalid

### S-12: is reachable when it has a reachable episode

- **Given** the system is in a standard operational state
- **When** it has a reachable episode
- **Then** is reachable

### S-13: is reachable when it has a reachable episode even if it is unpublished

- **Given** the system is in a standard operational state
- **When** it has a reachable episode even if it is unpublished
- **Then** is reachable

