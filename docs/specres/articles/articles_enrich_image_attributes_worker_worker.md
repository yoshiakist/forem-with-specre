---
id: "01KHY7PZMX7TNHYH4NFJRCSVJ6"
name: "articles_enrich_image_attributes_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/articles/enrich_image_attributes_worker.rb
- app/controllers/admin/articles_controller.rb
- app/controllers/api/v0/articles_controller.rb
- app/controllers/api/v1/articles_controller.rb
- app/controllers/api/v1/recommended_articles_lists_controller.rb
- app/controllers/articles_controller.rb
- app/controllers/concerns/api/articles_controller.rb
- app/controllers/stories/articles_search_controller.rb
- app/controllers/stories/pinned_articles_controller.rb
- app/controllers/stories/tagged_articles_controller.rb
- app/helpers/articles_helper.rb
- spec/workers/articles/enrich_image_attributes_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::EnrichImageAttributesWorker` within the articles domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **with article**: calls only Articles::EnrichImageAttributes
- **without article**: calls only Articles::EnrichImageAttributes

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/articles/enrich_image_attributes_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/recommended_articles_lists_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/articles_search_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/pinned_articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/tagged_articles_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/articles_helper.rb` -- shared view utility methods


## Scenarios

### S-1: calls only Articles::EnrichImageAttributes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls only Articles::EnrichImageAttributes

### S-2: calls both Articles::EnrichImageAttributes and EdgeCache::BustArticle if an anim...

- **Given** an animated image is detected
- **When** the action is triggered
- **Then** calls both Articles::EnrichImageAttributes and EdgeCache::BustArticle

### S-3: does not error

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not error

### S-4: does not call Articles::EnrichImageAttributes

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call Articles::EnrichImageAttributes

### S-5: does not call EdgeCache::BustArticle

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call EdgeCache::BustArticle

