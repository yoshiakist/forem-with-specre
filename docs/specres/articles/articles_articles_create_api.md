---
id: "01KHY7PZF2DS1VW1BDJKS3JE4E"
name: "articles_articles_create_api"
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
- spec/requests/articles/articles_create_spec.rb

## Functional Overview

This specification defines the expected behavior of `"ArticlesCreate"` within the articles domain.

### Behavioral Areas

- **ArticlesCreate**: Ensures correct behavior under the specified conditions
- **when scheduling jobs**: creates series when series is created with frontmatter
- **when creation limit is reached**: creates series when series is created with frontmatter
- **when setting published_at in editor v2**: creates series when series is created with frontmatter
- **when setting published_at from editor v1**: creates series when series is created with frontmatter
- **when validation error**: creates series when series is created with frontmatter

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

### S-1: creates ordinary article with proper params

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates ordinary article with proper params

### S-2: properly downcase tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** properly downcase tags

### S-3: creates article with front matter params

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates article with front matter params

### S-4: creates article with front matter params and org

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates article with front matter params and org

### S-5: creates series when series is created with frontmatter

- **Given** the system is in a standard operational state
- **When** series is created with frontmatter
- **Then** creates series

### S-6: returns the ID and the current_state_path of the article

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the ID and the current_state_path of the article

### S-7: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-8: returns a too_many_requests response if antispam rate limit is reached

- **Given** antispam rate limit is reached
- **When** the action is triggered
- **Then** returns a too_many_requests response

### S-9: returns a too_many_requests response if rate limit is reached

- **Given** rate limit is reached
- **When** the action is triggered
- **Then** returns a too_many_requests response

### S-10: sets published_at according to the timezone new

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets published_at according to the timezone new

### S-11: sets published_at for another timezone new

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets published_at for another timezone new

### S-12: sets published_at when only date is passed

- **Given** the system is in a standard operational state
- **When** only date is passed
- **Then** sets published_at

