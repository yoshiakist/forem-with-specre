---
id: "01KHY7PZHSFF8WP6ZAXAYQGC7N"
name: "articles_page_view_updater_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/articles/page_view_updater.rb
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
- spec/services/articles/page_view_updater_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::PageViewUpdater` within the articles domain.

### Behavioral Areas

- **call**: Ensures correct behavior under the specified conditions
- **when article published and written by another user**: updates a user
- **when article is unpublished**: sends a feed event journey when it receives a page view length of 60
- **when article written by given user**: updates a user
- **when time count equals EXTENDED_PAGEVIEW_NUMBER**: sends a feed event journey when it receives a page view length of 60

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/articles/page_view_updater.rb` -- business logic orchestration and domain operations
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

### S-1: updates a user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates a user

### S-2: skips updating

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** skips updating

### S-3: skips updating

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** skips updating

### S-4: sends a feed event journey when it receives a page view length of 60

- **Given** the system is in a standard operational state
- **When** it receives a page view length of 60
- **Then** sends a feed event journey

### S-5: does not send feed event journey when it receives a page view length of less tha...

- **Given** the system is in a standard operational state
- **When** it receives a page view length of less than 60
- **Then** does not send feed event journey

### S-6: only sends one event when it passes through the 60 range

- **Given** the system is in a standard operational state
- **When** it passes through the 60 range
- **Then** only sends one event

