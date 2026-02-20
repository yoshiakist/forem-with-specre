---
id: "01KHY7PZJ12A4RH5QTYQ84BH29"
name: "articles_unpublish_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/articles/unpublish.rb
- app/services/moderator/unpublish_all_articles.rb
- app/workers/moderator/unpublish_all_articles_worker.rb
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
- spec/services/articles/unpublish_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::Unpublish` within the articles domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/articles/unpublish.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/moderator/unpublish_all_articles.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/moderator/unpublish_all_articles_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/recommended_articles_lists_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/articles_search_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/pinned_articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/tagged_articles_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: unpublishes article without frontmatter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** unpublishes article without frontmatter

### S-2: unpublishes article with frontmatter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** unpublishes article with frontmatter

