---
id: "01KHY7PZDNBBQ91CB9AWAPZMJS"
name: "articles_feeds_relevancy_lever_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/articles/feeds/relevancy_lever.rb
- app/models/articles/feeds.rb
- app/models/articles/feeds/lever_catalog_builder.rb
- app/models/articles/feeds/order_by_lever.rb
- app/models/articles/feeds/variant_assembler.rb
- app/services/articles/feeds/article_score_calculator_for_user.rb
- app/services/articles/feeds/basic.rb
- app/services/articles/feeds/custom.rb
- app/services/articles/feeds/find_featured_story.rb
- app/services/articles/feeds/large_forem_experimental.rb
- app/services/articles/feeds/latest.rb
- spec/models/articles/feeds/relevancy_lever_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::Feeds::RelevancyLever` within the articles domain.

### Behavioral Areas

- **configure_with**: Ensures correct behavior under the specified conditions
- **when fallback is not a number**: raises InvalidQueryParametersError when not provided
- **when cases is not an array**: raises InvalidQueryParametersError when not provided
- **when cases includes a non-number**: raises InvalidQueryParametersError when not provided
- **when lever has query parameters**: sets the configured query parameters

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/articles/feeds/relevancy_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/lever_catalog_builder.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/order_by_lever.rb` -- data persistence, validations, and associations
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

- respond to :key
- respond to :label
- respond to :select fragment
- respond to :joins fragments
- respond to :group by fragment
- respond to :user required
- respond to :user required?

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: sets the configured query parameters

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the configured query parameters

### S-3: raises InvalidQueryParametersError when not provided

- **Given** the system is in a standard operational state
- **When** not provided
- **Then** raises InvalidQueryParametersError

