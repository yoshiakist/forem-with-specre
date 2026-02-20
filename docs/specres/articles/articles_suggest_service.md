---
id: "01KHY7PZHWWDT1AJRACBRAMVK3"
name: "articles_suggest_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/articles/suggest.rb
- app/services/articles/suggest_stickies.rb
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
- spec/services/articles/suggest_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::Suggest` within the articles domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/articles/suggest.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/suggest_stickies.rb` -- business logic orchestration and domain operations
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

### S-1: returns proper number of articles with post with the same tags

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns proper number of articles with post with the same tags

### S-2: returns proper number of articles with post with different tags

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns proper number of articles with post with different tags

### S-3: returns proper number of articles with post without tags

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns proper number of articles with post without tags

### S-4: returns the number of articles requested

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the number of articles requested

