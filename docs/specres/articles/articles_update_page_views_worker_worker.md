---
id: "01KHY7PZNC2ZPBGCGZT096S53N"
name: "articles_update_page_views_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/articles/update_page_views_worker.rb
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
- spec/workers/articles/update_page_views_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::UpdatePageViewsWorker` within the articles domain.

### Behavioral Areas

- **when the article is unpublished**: does not attempt to create a page view for an invalid article
- **when the article is published and written by the given user**: does not attempt to create a page view for an invalid article
- **when the article id is invalid**: does not attempt to create a page view for an invalid article
- **when the article exists**: does not attempt to create a page view for an invalid article
- **and the referrer is Google**: Ensures correct behavior under the specified conditions
- **and the referrer is not Google**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/articles/update_page_views_worker.rb` -- asynchronous job processing
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

### S-1: does not create a page view

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create a page view

### S-2: does not create a page view

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create a page view

### S-3: exits gracefully

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** exits gracefully

### S-4: does not attempt to create a page view for an invalid article

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not attempt to create a page view for an invalid article

### S-5: creates a page view

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a page view

### S-6: calls UpdateOrganicPageViewsWorker

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls UpdateOrganicPageViewsWorker

### S-7: creates a page view

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a page view

### S-8: does not call UpdateOrganicPageViewsWorker

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not call UpdateOrganicPageViewsWorker

