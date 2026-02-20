---
id: "01KHY7PZGJ9ZTH0MCE8AKZ7HTE"
name: "articles_builder_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/articles/feeds/lever_catalog_builder.rb
- app/services/articles/builder.rb
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
- spec/services/articles/builder_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::Builder` within the articles domain.

### Behavioral Areas

- **when tag_user_editor_v2**: Ensures correct behavior under the specified conditions
- **when tag_user**: Ensures correct behavior under the specified conditions
- **when prefill_user_editor_v2**: Ensures correct behavior under the specified conditions
- **when prefill_user**: Ensures correct behavior under the specified conditions
- **when tag**: Ensures correct behavior under the specified conditions
- **when user_editor_v2**: Ensures correct behavior under the specified conditions
- **when user_editor_v1**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/articles/feeds/lever_catalog_builder.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/articles/builder.rb` -- business logic orchestration and domain operations
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

### S-1: initializes an article with the correct attributes and needs authorization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** initializes an article with the correct attributes and needs authorization

### S-2: initializes an article with the correct attributes and needs authorization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** initializes an article with the correct attributes and needs authorization

### S-3: initializes an article with the correct attributes and needs authorization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** initializes an article with the correct attributes and needs authorization

### S-4: initializes an article with the correct attributes and needs authorization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** initializes an article with the correct attributes and needs authorization

### S-5: initializes an article with the correct attributes and does not need authorizati...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** initializes an article with the correct attributes and does not need authorization

### S-6: initializes an article with the correct attributes and does not need authorizati...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** initializes an article with the correct attributes and does not need authorization

### S-7: initializes an article with the correct attributes and does not need authorizati...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** initializes an article with the correct attributes and does not need authorization

