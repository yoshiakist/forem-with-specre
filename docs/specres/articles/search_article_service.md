---
id: "01KHY7PZK1HM7X9MSTX3VJW2QN"
name: "search_article_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/articles_controller.rb
- app/controllers/api/v0/articles_controller.rb
- app/controllers/api/v1/articles_controller.rb
- app/controllers/api/v1/recommended_articles_lists_controller.rb
- app/controllers/article_approvals_controller.rb
- app/controllers/articles_controller.rb
- app/controllers/concerns/api/articles_controller.rb
- app/controllers/stories/articles_search_controller.rb
- app/controllers/stories/pinned_articles_controller.rb
- app/controllers/stories/tagged_articles_controller.rb
- app/decorators/article_decorator.rb
- app/helpers/articles_helper.rb
- app/models/article.rb
- app/models/concerns/algolia_searchable/searchable_article.rb
- app/models/pinned_article.rb
- spec/services/search/article_spec.rb

## Functional Overview

This specification defines the expected behavior of `Search::Article` within the articles domain.

### Behavioral Areas

- **::search_documents**: Ensures correct behavior under the specified conditions
- **when describing the result format**: returns an empty result if there are no articles
- **when filtering by user_id**: returns no items when out of pagination bounds
- **when searching for a term**: sorts by title, tags, body ranking by default with a search term
- **when sorting**: supports sorting by published_at in ascending and descending order with a search term
- **when paginating**: returns no items when out of pagination bounds

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/recommended_articles_lists_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/article_approvals_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/articles_search_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/pinned_articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/tagged_articles_controller.rb` -- HTTP request routing and response handling
- **Decorator**: `app/decorators/article_decorator.rb` -- presentation logic and view-model enrichment
- **View helper**: `app/helpers/articles_helper.rb` -- shared view utility methods


## Scenarios

### S-1: returns an empty result if there are no articles

- **Given** there are no articles
- **When** the action is triggered
- **Then** returns an empty result

### S-2: does not return unpublished articles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not return unpublished articles

### S-3: returns published articles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns published articles

### S-4: does not include a highlight attribute

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not include a highlight attribute

### S-5: returns articles belonging to a specific user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns articles belonging to a specific user

### S-6: matches against the article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** matches against the article

### S-7: matches against the article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** matches against the article

### S-8: matches against the article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** matches against the article

### S-9: matches against the article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** matches against the article

### S-10: matches against the article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** matches against the article

### S-11: matches against the article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** matches against the article

### S-12: sorts by title, tags, body ranking by default with a search term

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sorts by title, tags, body ranking by default with a search term

