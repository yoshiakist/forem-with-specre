---
id: "01KHY7PZM1DYE3RNWXGH45FHFJ"
name: "articles_user_visits_articles_by_tag_system"
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
- spec/system/articles/user_visits_articles_by_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `"User` within the articles domain.

### Behavioral Areas

- **User visits articles by tag**: shows correct articles count
- **when user hasn**: Ensures correct behavior under the specified conditions
- **when 2 articles**: shows correct articles count
- **when more articles**: shows correct articles count
- **when user has logged in**: Ensures correct behavior under the specified conditions

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

### S-1: /t/javascript

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /t/javascript

### S-2: shows the header

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the header

### S-3: shows the follow button

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the follow button

### S-4: does not display a comment count of 0

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not display a comment count of 0

### S-5: shows correct articles count

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows correct articles count

### S-6: shows the correct articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the correct articles

### S-7: visits ok

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** visits ok

### S-8: /t/javascript

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /t/javascript

### S-9: /t/functional

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /t/functional

### S-10: shows the following button

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the following button

### S-11: shows top level sort options

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows top level sort options

