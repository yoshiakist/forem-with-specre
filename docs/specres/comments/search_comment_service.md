---
id: "01KHY7PZR66MKDV9CHBCY4BQJR"
name: "search_comment_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/comments_controller.rb
- app/controllers/api/v0/comments_controller.rb
- app/controllers/api/v1/comments_controller.rb
- app/controllers/comments_controller.rb
- app/controllers/concerns/api/comments_controller.rb
- app/decorators/comment_decorator.rb
- app/helpers/comments_helper.rb
- app/liquid_tags/comment_tag.rb
- app/models/comment.rb
- app/models/concerns/algolia_searchable/searchable_comment.rb
- app/policies/comment_policy.rb
- app/sanitizers/comment_email_scrubber.rb
- app/serializers/search/comment_serializer.rb
- app/services/ai/comment_check.rb
- app/services/ai/comment_helpfulness_assessor.rb
- spec/services/search/comment_spec.rb

## Functional Overview

This specification defines the expected behavior of `Search::Comment` within the comments domain.

### Behavioral Areas

- **::search_documents**: Ensures correct behavior under the specified conditions
- **when filtering Commentables**: returns no results when out of pagination bounds
- **when describing the result format**: returns the correct attributes for the result
- **when searching for a term**: returns no results when out of pagination bounds
- **when paginating**: returns no results when out of pagination bounds

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/comments_controller.rb` -- HTTP request routing and response handling
- **Decorator**: `app/decorators/comment_decorator.rb` -- presentation logic and view-model enrichment
- **View helper**: `app/helpers/comments_helper.rb` -- shared view utility methods
- **Liquid tag**: `app/liquid_tags/comment_tag.rb` -- custom Markdown/Liquid embed rendering
- **Model layer**: `app/models/comment.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_comment.rb` -- data persistence, validations, and associations
- **Policy layer**: `app/policies/comment_policy.rb` -- authorization and access control rules
- `app/sanitizers/comment_email_scrubber.rb`


## Scenarios

### S-1: does not include comments from Articles that are unpublished

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not include comments from Articles that are unpublished

### S-2: returns the correct attributes for the result

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct attributes for the result

### S-3: returns the correct attributes for the user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct attributes for the user

### S-4: returns highlights

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns highlights

### S-5: orders the results by score (hotness_score) in descending order by default

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** orders the results by score (hotness_score) in descending order by default

### S-6: orders the results by published_at (created_at) in descending order

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** orders the results by published_at (created_at) in descending order

### S-7: orders the results by published_at (created_at) in ascending order

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** orders the results by published_at (created_at) in ascending order

### S-8: matches against the comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** matches against the comment

### S-9: returns no results when out of pagination bounds

- **Given** the system is in a standard operational state
- **When** out of pagination bounds
- **Then** returns no results

### S-10: returns paginated results

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns paginated results

