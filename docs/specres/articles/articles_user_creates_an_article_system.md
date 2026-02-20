---
id: "01KHY7PZKHS6BGGHV05TN9TRH3"
name: "articles_user_creates_an_article_system"
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
- spec/system/articles/user_creates_an_article_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Creating` within the articles domain.

### Behavioral Areas

- **Creating an article with the editor**: creates a new article
- **with runkit_tag**: creates a new article with a Runkit tag
- **with an active announcement**: does not render the announcement broadcast
- **with Runkit tag**: creates a new article with a Runkit tag
- **when user creates too many articles**: creates a new article

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

### S-1: creates a new article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new article

### S-2: does not render the announcement broadcast

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not render the announcement broadcast

### S-3: creates a new article with a Runkit tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new article with a Runkit tag

### S-4: creates a new article with a Runkit tag with complex preamble

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new article with a Runkit tag with complex preamble

### S-5: previews article with a Runkit tag and creates it

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** previews article with a Runkit tag and creates it

### S-6: displays a rate limit warning

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays a rate limit warning

