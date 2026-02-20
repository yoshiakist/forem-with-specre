---
id: "01KHY7PZE8BXXP3V6GSDMH8AEV"
name: "articles_active_threads_query_query"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/queries/articles/active_threads_query.rb
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
- spec/queries/articles/active_threads_query_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::ActiveThreadsQuery` within the articles domain.

### Behavioral Areas

- **::call**: Ensures correct behavior under the specified conditions
- **when time_ago is latest**: returns the latest article with a good score
- **when given a precise time**: returns article ordered_by comment_count based on time
- **when time_ago is not given**: respects published_at threshold of 3 days when time_ago is nil

### Implementation Architecture

The behavior is implemented across the following layers:

- **Query object**: `app/queries/articles/active_threads_query.rb` -- complex database query encapsulation
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

### S-1: returns the latest article with a good score

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the latest article with a good score

### S-2: does not return articles below the minimum score threshold

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not return articles below the minimum score threshold

### S-3: returns only articles at or above the minimum score

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns only articles at or above the minimum score

### S-4: returns article ordered_by comment_count based on time

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns article ordered_by comment_count based on time

### S-5: excludes articles below minimum score even with high comment counts

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** excludes articles below minimum score even with high comment counts

### S-6: respects both time and score filters

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** respects both time and score filters

### S-7: returns articles ordered by last_comment_at, not based on time

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns articles ordered by last_comment_at, not based on time

### S-8: excludes articles below minimum score regardless of last_comment_at

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** excludes articles below minimum score regardless of last_comment_at

### S-9: respects published_at threshold of 3 days when time_ago is nil

- **Given** the system is in a standard operational state
- **When** time_ago is nil
- **Then** respects published_at threshold of 3 days

