---
id: "01KHY7PZF5SN5M4QHHPSK9T3SP"
name: "articles_articles_destroy_api"
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
- spec/requests/articles/articles_destroy_spec.rb

## Functional Overview

This specification defines the expected behavior of `"ArticlesDestroy"` within the articles domain.

### Behavioral Areas

- **ArticlesDestroy**: Ensures correct behavior under the specified conditions
- **when DELETE /articles/:slug**: Ensures correct behavior under the specified conditions
- **when GET /delete_confirm**: Ensures correct behavior under the specified conditions
- **without an article**: destroyed an article
- **with an article the current user wrote**: destroyed an article
- **when an admin attempts to delete an article**: destroyed an article
- **when another user attempts to delete someone**: Ensures correct behavior under the specified conditions

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


## Scenarios

### S-1: destroyed an article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** destroyed an article

### S-2: schedules a RemoveAllWorker if there are comments

- **Given** there are comments
- **When** the action is triggered
- **Then** schedules a RemoveAllWorker

### S-3: removes all previous published notifications

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes all previous published notifications

### S-4: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-5: renders not_found

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders not_found

### S-6: renders success

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders success

### S-7: renders success

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders success

### S-8: raises a policy error

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises a policy error

