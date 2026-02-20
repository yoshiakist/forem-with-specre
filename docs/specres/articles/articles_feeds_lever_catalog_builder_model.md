---
id: "01KHY7PZDG1FFQ9ZBAMKD2R1DS"
name: "articles_feeds_lever_catalog_builder_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/articles/feeds/lever_catalog_builder.rb
- app/models/articles/feeds.rb
- app/models/articles/feeds/order_by_lever.rb
- app/models/articles/feeds/relevancy_lever.rb
- app/models/articles/feeds/variant_assembler.rb
- app/services/articles/feeds/article_score_calculator_for_user.rb
- app/services/articles/feeds/basic.rb
- app/services/articles/feeds/custom.rb
- app/services/articles/feeds/find_featured_story.rb
- app/services/articles/feeds/large_forem_experimental.rb
- app/services/articles/feeds/latest.rb
- spec/models/articles/feeds/lever_catalog_builder_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::Feeds::LeverCatalogBuilder` within the articles domain.

### Behavioral Areas

- **.new**: Ensures correct behavior under the specified conditions
- **fetch_lever**: Ensures correct behavior under the specified conditions
- **when lever exists**: raise a DuplicateLeverError when configured with a duplicate relevancy_lever key
- **when lever does not exist**: raise a DuplicateLeverError when configured with a duplicate relevancy_lever key
- **fetch_order_by**: Ensures correct behavior under the specified conditions
- **when lever exists**: raise a DuplicateLeverError when configured with a duplicate relevancy_lever key
- **when lever does not exist**: raise a DuplicateLeverError when configured with a duplicate relevancy_lever key

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/articles/feeds/lever_catalog_builder.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/order_by_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/relevancy_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/variant_assembler.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/articles/feeds/article_score_calculator_for_user.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/basic.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/custom.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/find_featured_story.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/large_forem_experimental.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/latest.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- be a described class
- be frozen
- be a Articles::Feeds::RelevancyLever
- be frozen
- be a Articles::Feeds::OrderByLever
- be frozen

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: raise a DuplicateLeverError when configured with a duplicate relevancy_lever key

- **Given** the system is in a standard operational state
- **When** configured with a duplicate relevancy_lever key
- **Then** raise a DuplicateLeverError

### S-3: raise a DuplicateLeverError when configured with a duplicate order_by_lever key

- **Given** the system is in a standard operational state
- **When** configured with a duplicate order_by_lever key
- **Then** raise a DuplicateLeverError

