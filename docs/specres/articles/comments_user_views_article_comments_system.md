---
id: "01KHY7PZM8MSZ4PJMMCV1EFYAT"
name: "comments_user_views_article_comments_system"
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
- spec/system/comments/user_views_article_comments_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Visiting` within the articles domain.

### Behavioral Areas

- **Visiting article comments**: #{article.path}/comments
- **when all comments**: #{article.path}/comments
- **when root is specified**: Ensures correct behavior under the specified conditions
- **when looking into comment links**: #{article.path}/comments

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/recommended_articles_lists_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/article_approvals_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/articles_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: #{article.path}/comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** #{article.path}/comments

### S-2: displays comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays comments

### S-3: displays child comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays child comments

### S-4: displays grandchild comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays grandchild comments

### S-5: #{article.path}/comments/#{comment.id.to_s(26)}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** #{article.path}/comments/#{comment.id.to_s(26)}

### S-6: displays related comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays related comments

### S-7: displays child comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays child comments

### S-8: displays grandchild comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays grandchild comments

### S-9: uses the permalink for signed in users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses the permalink for signed in users

### S-10: uses an anchor tag instead of permalink for signed out users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses an anchor tag instead of permalink for signed out users

