---
id: "01KHY7PZDT42S0E2NZ3SYHSZJG"
name: "articles_feeds_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/articles/feeds.rb
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
- spec/models/articles/feeds_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::Feeds` within the articles domain.

### Behavioral Areas

- **.lever_catalog**: Ensures correct behavior under the specified conditions
- **.feed_for**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/articles/feeds.rb` -- data persistence, validations, and associations
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

### S-1: Data integrity and associations

The model enforces the following constraints:

- be a Articles::Feeds::LeverCatalogBuilder
- be frozen
- be a described class::VariantQuery

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: creates proper offset for page 2

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates proper offset for page 2

### S-3: creates proper offset for page 4

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates proper offset for page 4

### S-4: creates proper offset for page 1

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates proper offset for page 1

### S-5: creates proper offset for page 0

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates proper offset for page 0

