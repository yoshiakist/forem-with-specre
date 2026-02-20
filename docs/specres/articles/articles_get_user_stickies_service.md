---
id: "01KHY7PZHQK1TWEZQW9JFE4F1R"
name: "articles_get_user_stickies_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/articles/get_user_stickies.rb
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
- spec/services/articles/get_user_stickies_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::GetUserStickies` within the articles domain.

### Behavioral Areas

- **.call**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/articles/get_user_stickies.rb` -- business logic orchestration and domain operations
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

### S-1: returns articles with limited attributes needed by _sticky_nav

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns articles with limited attributes needed by _sticky_nav

### S-2: allows decorating for cached_tag_list_array (used in view)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows decorating for cached_tag_list_array (used in view)

### S-3: excludes the current article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** excludes the current article

### S-4: does not load unnecessary columns

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not load unnecessary columns

### S-5: handles article with nil cached_tag_list

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles article with nil cached_tag_list

