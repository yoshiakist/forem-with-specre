---
id: "01KHY7PZFQGFZH6E84R8Y2VZNZ"
name: "articles_api"
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
- app/models/recommended_articles_list.rb
- app/queries/homepage/articles_query.rb
- app/services/exporter/articles.rb
- app/services/homepage/fetch_articles.rb
- app/services/moderator/sink_articles.rb
- spec/requests/articles_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Articles"` within the articles domain.

### Behavioral Areas

- **Articles**: Ensures correct behavior under the specified conditions
- **default subforem_id assignment**: automatically assigns default subforem_id when creating an article

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
- **Model layer**: `app/models/recommended_articles_list.rb` -- data persistence, validations, and associations
- **Query object**: `app/queries/homepage/articles_query.rb` -- complex database query encapsulation


## Scenarios

### S-1: automatically assigns default subforem_id when creating an article

- **Given** the system is in a standard operational state
- **When** creating an article
- **Then** automatically assigns default subforem_id

### S-2: does not override explicitly set subforem_id

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not override explicitly set subforem_id

