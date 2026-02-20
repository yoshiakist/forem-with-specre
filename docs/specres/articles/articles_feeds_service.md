---
id: "01KHY7PZHMNSH06J1QPF8HQP72"
name: "articles_feeds_service"
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
- spec/services/articles/feeds_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::Feeds` within the articles domain.

### Behavioral Areas

- **NUMBER_OF_HOURS_TO_OFFSET_USERS_LATEST_ARTICLE_VIEWS**: sets NUMBER_OF_HOURS_TO_OFFSET_USERS_LATEST_ARTICLE_VIEWS to ApplicationConfig
- **.oldest_published_at_to_consider_for**: Ensures correct behavior under the specified conditions
- **when the given user is nil**: sets NUMBER_OF_HOURS_TO_OFFSET_USERS_LATEST_ARTICLE_VIEWS to ApplicationConfig
- **when the given user has no page views**: sets NUMBER_OF_HOURS_TO_OFFSET_USERS_LATEST_ARTICLE_VIEWS to ApplicationConfig
- **when the user has recent page views**: sets NUMBER_OF_HOURS_TO_OFFSET_USERS_LATEST_ARTICLE_VIEWS to ApplicationConfig
- **when the user has very old page views**: sets NUMBER_OF_HOURS_TO_OFFSET_USERS_LATEST_ARTICLE_VIEWS to ApplicationConfig

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

- be a ActiveSupport::TimeWithZone
- eq expected result
- be within 24.hours.of expected result

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: sets NUMBER_OF_HOURS_TO_OFFSET_USERS_LATEST_ARTICLE_VIEWS to ApplicationConfig

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets NUMBER_OF_HOURS_TO_OFFSET_USERS_LATEST_ARTICLE_VIEWS to ApplicationConfig

### S-3: returns default 18 when ApplicationConfig is not defined

- **Given** the system is in a standard operational state
- **When** ApplicationConfig is not defined
- **Then** returns default 18

### S-4: returns Article::Feeds::DEFAULT_DAYS_SINCE_PUBLISHED days ago

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns Article::Feeds::DEFAULT_DAYS_SINCE_PUBLISHED days ago

