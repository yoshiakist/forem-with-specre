---
id: "01KHY7PZGM9YVY76DP510RV8NV"
name: "articles_creator_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/articles/creator.rb
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
- spec/services/articles/creator_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::Creator` within the articles domain.

### Behavioral Areas

- **when valid attributes**: creates an organization collection when series and organization_id are provided
- **when invalid attributes**: creates an organization collection when series and organization_id are provided
- **when creating a published article**: creates an article
- **when creating a not-yet-published article**: creates an article
- **when creating a non-published article**: creates an article
- **with organization collections**: creates an organization collection when series and organization_id are provided

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/articles/creator.rb` -- business logic orchestration and domain operations
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

### S-1: creates an article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an article

### S-2: returns a non decorated, persisted article

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a non decorated, persisted article

### S-3: creates a notification subscription

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a notification subscription

### S-4: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-5: returns a non decorated, non persisted article

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a non decorated, non persisted article

### S-6: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-7: refreshes user segments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** refreshes user segments

### S-8: does not refresh user segments

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not refresh user segments

### S-9: does not refresh user segments

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not refresh user segments

### S-10: creates an organization collection when series and organization_id are provided

- **Given** the system is in a standard operational state
- **When** series and organization_id are provided
- **Then** creates an organization collection

### S-11: creates a personal collection when series is provided but no organization_id

- **Given** the system is in a standard operational state
- **When** series is provided but no organization_id
- **Then** creates a personal collection

### S-12: finds existing organization collection when series already exists

- **Given** the system is in a standard operational state
- **When** series already exists
- **Then** finds existing organization collection

