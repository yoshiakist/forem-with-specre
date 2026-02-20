---
id: "01KHY7PZJ3PCGQ3QKYGKC191E5"
name: "articles_updater_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/articles/page_view_updater.rb
- app/services/articles/updater.rb
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
- spec/services/articles/updater_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::Updater` within the articles domain.

### Behavioral Areas

- **with organization collections**: creates an organization collection when series is provided and article is under org
- **result**: Ensures correct behavior under the specified conditions
- **notifications**: destroys the preexisting notifications
- **when an article is updated and published the first time**: updates an article
- **when an article is being updated (published => published)**: updates an article
- **when an article is being republished**: updates an article
- **when an article is being unpublished from frontmatter**: updates an article
- **when an article is being unpublished**: updates an article

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/articles/page_view_updater.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/updater.rb` -- business logic orchestration and domain operations
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

### S-1: updates an article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates an article

### S-2: sets a collection

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets a collection

### S-3: creates a collection for the user, not admin when updated by admin

- **Given** the system is in a standard operational state
- **When** updated by admin
- **Then** creates a collection for the user, not admin

### S-4: creates an organization collection when series is provided and article is under ...

- **Given** the system is in a standard operational state
- **When** series is provided and article is under org
- **Then** creates an organization collection

### S-5: creates a personal collection when series is provided and article has no org

- **Given** the system is in a standard operational state
- **When** series is provided and article has no org
- **Then** creates a personal collection

### S-6: updates collection when organization_id changes

- **Given** the system is in a standard operational state
- **When** organization_id changes
- **Then** updates collection

### S-7: finds existing organization collection regardless of user_id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** finds existing organization collection regardless of user_id

### S-8: sets tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets tags

### S-9: returns success when saved

- **Given** the system is in a standard operational state
- **When** saved
- **Then** returns success

### S-10: returns not success when not saved

- **Given** the system is in a standard operational state
- **When** not saved
- **Then** returns not success

### S-11: sets current published_at when publishing from a draft

- **Given** the system is in a standard operational state
- **When** publishing from a draft
- **Then** sets current published_at

### S-12: sets the passed published_at when a future published_at is passed

- **Given** the system is in a standard operational state
- **When** a future published_at is passed
- **Then** sets the passed published_at

