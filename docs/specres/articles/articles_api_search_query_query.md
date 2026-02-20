---
id: "01KHY7PZEA52K6B0Y3V80W9B7T"
name: "articles_api_search_query_query"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/queries/articles/api_search_query.rb
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
- spec/queries/articles/api_search_query_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::ApiSearchQuery` within the articles domain.

### Behavioral Areas

- **when there is no query parameter**: shows articles that match that query
- **when there is a query parameter**: shows articles that match that query
- **when there is a top parameter**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Query object**: `app/queries/articles/api_search_query.rb` -- complex database query encapsulation
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

### S-1: shows all published and approved articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows all published and approved articles

### S-2: shows articles that match that query

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows articles that match that query

### S-3: does not show article if below minimum index

- **Given** below minimum index
- **When** the action is triggered
- **Then** does not show article

### S-4: shows the most popular articles in the last n days

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the most popular articles in the last n days

