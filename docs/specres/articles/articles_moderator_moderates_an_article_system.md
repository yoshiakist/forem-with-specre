---
id: "01KHY7PZKE5Y9YHP1BDDS28JQP"
name: "articles_moderator_moderates_an_article_system"
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
- spec/system/articles/moderator_moderates_an_article_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Views` within the articles domain.

### Behavioral Areas

- **Views an article**: /#{user.username}/#{article.slug}/mod

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

### S-1: /#{user.username}/#{article.slug}/mod

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{user.username}/#{article.slug}/mod

### S-2: shows an article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows an article

### S-3: /#{user.username}/#{article.slug}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{user.username}/#{article.slug}

### S-4: lets moderators visit /mod

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** lets moderators visit /mod

### S-5: /#{user.username}/#{article.slug}/mod

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{user.username}/#{article.slug}/mod

### S-6: shows hidden comments on /mod

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows hidden comments on /mod

### S-7: /#{user.username}/#{article.slug}/mod

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{user.username}/#{article.slug}/mod

