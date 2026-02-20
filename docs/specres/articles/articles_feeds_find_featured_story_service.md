---
id: "01KHY7PZH5A1A397WAXJC8EMZW"
name: "articles_feeds_find_featured_story_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/articles/feeds/find_featured_story.rb
- app/models/articles/feeds.rb
- app/models/articles/feeds/lever_catalog_builder.rb
- app/models/articles/feeds/order_by_lever.rb
- app/models/articles/feeds/relevancy_lever.rb
- app/models/articles/feeds/variant_assembler.rb
- app/services/articles/feeds/article_score_calculator_for_user.rb
- app/services/articles/feeds/basic.rb
- app/services/articles/feeds/custom.rb
- app/services/articles/feeds/large_forem_experimental.rb
- app/services/articles/feeds/latest.rb
- spec/services/articles/feeds/find_featured_story_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::Feeds::FindFeaturedStory` within the articles domain.

### Behavioral Areas

- **when passed an ActiveRecord collection**: Ensures correct behavior under the specified conditions
- **when must_have_main_image is false**: Ensures correct behavior under the specified conditions
- **when passed an array**: Ensures correct behavior under the specified conditions
- **when must_have_main_image is false**: Ensures correct behavior under the specified conditions
- **when passed collection without any articles**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/articles/feeds/find_featured_story.rb` -- business logic orchestration and domain operations
- **Model layer**: `app/models/articles/feeds.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/lever_catalog_builder.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/order_by_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/relevancy_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/variant_assembler.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/articles/feeds/article_score_calculator_for_user.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/basic.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/custom.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/large_forem_experimental.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/latest.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns first article with a main image

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns first article with a main image

### S-2: returns the first article

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the first article

### S-3: returns first article with a main image

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns first article with a main image

### S-4: returns the first article

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the first article

### S-5: returns an new, empty Article object

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an new, empty Article object

