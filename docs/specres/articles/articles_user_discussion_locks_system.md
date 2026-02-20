---
id: "01KHY7PZKPG9429W94NGTHFP5B"
name: "articles_user_discussion_locks_system"
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
- spec/system/articles/user_discussion_locks_spec.rb

## Functional Overview

This specification defines the expected behavior of `"User` within the articles domain.

### Behavioral Areas

- **User discussion locks**: shows the discussion lock button in manage
- **when an Article does not have a discussion lock**: shows the discussion lock button in manage
- **when an Article has a discussion lock**: shows the discussion lock button in manage

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

### S-1: shows the discussion lock button in manage

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the discussion lock button in manage

### S-2: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-3: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-4: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-5: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-6: #{article.path}/comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** #{article.path}/comments

### S-7: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-8: #{article.path}/comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** #{article.path}/comments

### S-9: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-10: #{article.path}/comments/#{comment_one.id.to_s(26)}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** #{article.path}/comments/#{comment_one.id.to_s(26)}

### S-11: #{article.path}/comments/#{comment_two.id.to_s(26)}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** #{article.path}/comments/#{comment_two.id.to_s(26)}

### S-12: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

