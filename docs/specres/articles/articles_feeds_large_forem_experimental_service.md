---
id: "01KHY7PZH7DJRAX2D76WYY7RGK"
name: "articles_feeds_large_forem_experimental_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/articles/feeds/large_forem_experimental.rb
- app/models/articles/feeds.rb
- app/models/articles/feeds/lever_catalog_builder.rb
- app/models/articles/feeds/order_by_lever.rb
- app/models/articles/feeds/relevancy_lever.rb
- app/models/articles/feeds/variant_assembler.rb
- app/services/articles/feeds/article_score_calculator_for_user.rb
- app/services/articles/feeds/basic.rb
- app/services/articles/feeds/custom.rb
- app/services/articles/feeds/find_featured_story.rb
- app/services/articles/feeds/latest.rb
- spec/services/articles/feeds/large_forem_experimental_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::Feeds::LargeForemExperimental` within the articles domain.

### Behavioral Areas

- **featured_story_and_default_home_feed**: Ensures correct behavior under the specified conditions
- **when user logged in**: Ensures correct behavior under the specified conditions
- **when ranking is true**: performs article ranking
- **when ranking is false**: performs article ranking
- **when ranking not passed**: performs article ranking
- **default_home_feed**: Ensures correct behavior under the specified conditions
- **when user is not logged in**: Ensures correct behavior under the specified conditions
- **when user logged in**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/articles/feeds/large_forem_experimental.rb` -- business logic orchestration and domain operations
- **Model layer**: `app/models/articles/feeds.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/lever_catalog_builder.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/order_by_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/relevancy_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/variant_assembler.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/articles/feeds/article_score_calculator_for_user.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/basic.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/custom.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/find_featured_story.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/latest.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns a featured article and correctly scored other articles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a featured article and correctly scored other articles

### S-2: only includes stories

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** only includes stories

### S-3: does not load blocked articles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not load blocked articles

### S-4: performs article ranking

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** performs article ranking

### S-5: does not perform article ranking

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not perform article ranking

### S-6: performs article ranking

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** performs article ranking

### S-7: returns array of high scoring articles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns array of high scoring articles

### S-8: includes stories

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes stories

### S-9: works with every variant

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** works with every variant

### S-10: returns articles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns articles

### S-11: only returns the requested number of articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** only returns the requested number of articles

### S-12: returns articles in scored order

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns articles in scored order

