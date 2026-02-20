---
id: "01KHY7PZMNGVHTFKPB0RWT9TXG"
name: "articles_view"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

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
- app/models/recommended_articles_list.rb
- app/queries/homepage/articles_query.rb
- app/services/exporter/articles.rb
- app/services/homepage/fetch_articles.rb
- app/services/moderator/sink_articles.rb
- spec/views/articles_spec.rb

## Functional Overview

This specification defines the expected behavior of `"articles/show"` within the articles domain.

### Behavioral Areas

- **articles/show**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

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
- **Model layer**: `app/models/recommended_articles_list.rb` -- data persistence, validations, and associations
- **Query object**: `app/queries/homepage/articles_query.rb` -- complex database query encapsulation


## Scenarios

### S-1: shows user title of the article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows user title of the article

### S-2: shows user tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows user tags

### S-3: shows user content of the article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows user content of the article

### S-4: shows user new comment box

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows user new comment box

### S-5: shows a note about the canonical URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows a note about the canonical URL

### S-6: shows a note about the canonical URL after edit

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows a note about the canonical URL after edit

### S-7: shows the original publication time for crossposts

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the original publication time for crossposts

