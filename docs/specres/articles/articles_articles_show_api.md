---
id: "01KHY7PZFA286CDSNTP63WXT07"
name: "articles_articles_show_api"
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
- spec/requests/articles/articles_show_spec.rb

## Functional Overview

This specification defines the expected behavior of `"ArticlesShow"` within the articles domain.

### Behavioral Areas

- **ArticlesShow**: Ensures correct behavior under the specified conditions
- **GET /:slug (articles)**: Ensures correct behavior under the specified conditions
- **GET /:username/:slug (scheduled)**: Ensures correct behavior under the specified conditions
- **when keywords are set**: returns a 200 status when navigating to the article
- **when keywords are not**: returns a 200 status when navigating to the article
- **when author has spam role**: returns a 200 status when navigating to the article
- **when user signed in**: returns a 200 status when navigating to the article
- **GET /:slug (user)**: Ensures correct behavior under the specified conditions

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

### S-1: returns a 200 status when navigating to the article

- **Given** the system is in a standard operational state
- **When** navigating to the article
- **Then** returns a 200 status

### S-2: renders the proper JSON-LD for an article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper JSON-LD for an article

### S-3: renders DiscussionForumPosting structured data when article has comments

- **Given** the system is in a standard operational state
- **When** article has comments
- **Then** renders DiscussionForumPosting structured data

### S-4: renders Comment structured data for article comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders Comment structured data for article comments

### S-5: renders nested comment structure for replies

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders nested comment structure for replies

### S-6: caches JSON-LD at view level based on last_comment_at

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** caches JSON-LD at view level based on last_comment_at

### S-7: renders 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders 

### S-8: renders a scheduled article with the article password

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders a scheduled article with the article password

### S-9: renders 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders 

### S-10: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-11: renders 404 for a scheduled article w/o article password

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders 404 for a scheduled article w/o article password

### S-12: renders the proper organization for an article when one is present

- **Given** the system is in a standard operational state
- **When** one is present
- **Then** renders the proper organization for an article

