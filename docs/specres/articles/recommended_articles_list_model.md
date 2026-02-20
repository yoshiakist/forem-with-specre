---
id: "01KHY7PZE09R80P57ZWTXHTNEP"
name: "recommended_articles_list_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/api/v1/recommended_articles_lists_controller.rb
- app/models/recommended_articles_list.rb
- app/models/article.rb
- app/models/articles/cached_entity.rb
- app/models/articles/feeds.rb
- app/models/articles/feeds/lever_catalog_builder.rb
- app/models/articles/feeds/order_by_lever.rb
- app/models/articles/feeds/relevancy_lever.rb
- app/models/articles/feeds/variant_assembler.rb
- app/models/concerns/algolia_searchable/searchable_article.rb
- app/models/pinned_article.rb
- spec/models/recommended_articles_list_spec.rb

## Functional Overview

This specification defines the expected behavior of `RecommendedArticlesList` within the articles domain.

### Behavioral Areas

- **associations**: Ensures correct behavior under the specified conditions
- **validations**: Ensures correct behavior under the specified conditions
- **.active**: Ensures correct behavior under the specified conditions
- **before_save**: Ensures correct behavior under the specified conditions
- **when expires_at is not set**: sets expires_at to one day from now
- **article_ids=**: Ensures correct behavior under the specified conditions
- **when input is a comma-separated string**: Ensures correct behavior under the specified conditions
- **when input is an array**: converts it to an array of integers

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/api/v1/recommended_articles_lists_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/recommended_articles_list.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/article.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/cached_entity.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/lever_catalog_builder.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/order_by_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/relevancy_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/variant_assembler.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_article.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/pinned_article.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to user
- validate presence of name
- validate length of name.is at most 120

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: includes lists that have not expired

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes lists that have not expired

### S-3: excludes lists that have expired

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** excludes lists that have expired

### S-4: sets expires_at to one day from now

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets expires_at to one day from now

### S-5: converts it to an array of integers

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** converts it to an array of integers

### S-6: keeps it as an array of integers

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** keeps it as an array of integers

### S-7: filters out invalid entries

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** filters out invalid entries

