---
id: "01KHY7PZKSCZ1BBJYDQ13JZ3TV"
name: "articles_user_edits_an_article_system"
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
- spec/system/articles/user_edits_an_article_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Editing` within the articles domain.

### Behavioral Areas

- **Editing with an editor**: Ensures correct behavior under the specified conditions
- **when user edits too many articles**: user previews their changes

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

### S-1: user previews their changes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** user previews their changes

### S-2: /#{user.username}/#{article.slug}/edit

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{user.username}/#{article.slug}/edit

### S-3: user updates their post

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** user updates their post

### S-4: /#{user.username}/#{article.slug}/edit

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{user.username}/#{article.slug}/edit

### S-5: user unpublishes their post

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** user unpublishes their post

### S-6: /#{user.username}/#{article.slug}/edit

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{user.username}/#{article.slug}/edit

### S-7: displays a rate limit warning

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays a rate limit warning

### S-8: /#{user.username}/#{article.slug}/edit

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{user.username}/#{article.slug}/edit

