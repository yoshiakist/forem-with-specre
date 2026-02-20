---
id: "01KHY7PZDRWC4HN8VT1SREG0AC"
name: "articles_feeds_variant_assembler_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/articles/feeds/variant_assembler.rb
- app/models/articles/feeds.rb
- app/models/articles/feeds/lever_catalog_builder.rb
- app/models/articles/feeds/order_by_lever.rb
- app/models/articles/feeds/relevancy_lever.rb
- app/services/articles/feeds/article_score_calculator_for_user.rb
- app/services/articles/feeds/basic.rb
- app/services/articles/feeds/custom.rb
- app/services/articles/feeds/find_featured_story.rb
- app/services/articles/feeds/large_forem_experimental.rb
- app/services/articles/feeds/latest.rb
- spec/models/articles/feeds/variant_assembler_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::Feeds::VariantAssembler` within the articles domain.

### Behavioral Areas

- **.user_config_hash_for**: Ensures correct behavior under the specified conditions
- **when #{variant.inspect}**: Ensures correct behavior under the specified conditions
- **when \**: Ensures correct behavior under the specified conditions
- **.call**: Ensures correct behavior under the specified conditions
- **when #{variant.inspect}**: Ensures correct behavior under the specified conditions
- **with missing variant**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/articles/feeds/variant_assembler.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/lever_catalog_builder.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/order_by_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/relevancy_lever.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/articles/feeds/article_score_calculator_for_user.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/basic.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/custom.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/find_featured_story.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/large_forem_experimental.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/latest.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- be a Hash
- be a Hash
- be a Articles::Feeds::VariantQuery::Config

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

