---
id: "01KHY7PZFDE4GF4TXX8YXQSJHN"
name: "articles_articles_api"
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
- spec/requests/articles/articles_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Articles"` within the articles domain.

### Behavioral Areas

- **Articles**: returns not found if no articles
- **GET /feed(/:username|/:tag_name)**: Ensures correct behavior under the specified conditions
- **with caching headers**: sets Fastly Cache-Control headers
- **when :username param is not given**: Ensures correct behavior under the specified conditions
- **when user/organization articles exist**: returns not found if no articles
- **when :username param is given and belongs to a user**: returns only articles for that user
- **when user/organization articles exist**: returns not found if no articles
- **when :username param is given and belongs to an organization**: returns only articles for that organization

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

### S-1: returns rss+xml content

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns rss+xml content

### S-2: contains the full app URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** contains the full app URL

### S-3: returns not found if no articles

- **Given** no articles
- **When** the action is triggered
- **Then** returns not found

### S-4: does not contain image tag

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not contain image tag

### S-5: sets Fastly Cache-Control headers

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets Fastly Cache-Control headers

### S-6: sets Fastly Surrogate-Control headers

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets Fastly Surrogate-Control headers

### S-7: sets Fastly Surrogate-Key headers

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets Fastly Surrogate-Key headers

### S-8: sets Nginx X-Accel-Expires headers

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets Nginx X-Accel-Expires headers

### S-9: returns only featured articles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns only featured articles

### S-10: returns only articles for that user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns only articles for that user

### S-11: contains user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** contains user

### S-12: returns only articles for that organization

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns only articles for that organization

