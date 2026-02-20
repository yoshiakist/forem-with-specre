---
id: "01KHY7PZGZR3HN4CHZJ3V2G7QP"
name: "articles_feeds_basic_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/articles/feeds/basic.rb
- app/models/articles/feeds.rb
- app/models/articles/feeds/lever_catalog_builder.rb
- app/models/articles/feeds/order_by_lever.rb
- app/models/articles/feeds/relevancy_lever.rb
- app/models/articles/feeds/variant_assembler.rb
- app/services/articles/feeds/article_score_calculator_for_user.rb
- app/services/articles/feeds/custom.rb
- app/services/articles/feeds/find_featured_story.rb
- app/services/articles/feeds/large_forem_experimental.rb
- app/services/articles/feeds/latest.rb
- spec/services/articles/feeds/basic_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::Feeds::Basic` within the articles domain.

### Behavioral Areas

- **without a user**: returns articles with score above 0 sorted by user preference scores
- **with a user**: returns articles with score above 0 in order of hotness score
- **when user has hidden tags**: returns articles with score above 0 sorted by user preference scores

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/articles/feeds/basic.rb` -- business logic orchestration and domain operations
- **Model layer**: `app/models/articles/feeds.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/lever_catalog_builder.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/order_by_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/relevancy_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/variant_assembler.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/articles/feeds/article_score_calculator_for_user.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/custom.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/find_featured_story.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/large_forem_experimental.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/latest.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns articles with score above 0 in order of hotness score

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns articles with score above 0 in order of hotness score

### S-2: returns articles with score above 0 sorted by user preference scores

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns articles with score above 0 sorted by user preference scores

### S-3: does not load blocked articles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not load blocked articles

### S-4: does not return articles with tags the user has hidden

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not return articles with tags the user has hidden

