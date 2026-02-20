---
id: "01KHY7PZDXZEEED6GWSRZX8D85"
name: "pinned_article_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/stories/pinned_articles_controller.rb
- app/models/pinned_article.rb
- app/policies/pinned_article_policy.rb
- app/models/article.rb
- app/models/articles/cached_entity.rb
- app/models/articles/feeds.rb
- app/models/articles/feeds/lever_catalog_builder.rb
- app/models/articles/feeds/order_by_lever.rb
- app/models/articles/feeds/relevancy_lever.rb
- app/models/articles/feeds/variant_assembler.rb
- app/models/concerns/algolia_searchable/searchable_article.rb
- app/models/recommended_articles_list.rb
- spec/models/pinned_article_spec.rb

## Functional Overview

This specification defines the expected behavior of `PinnedArticle` within the articles domain.

### Behavioral Areas

- **.exists?**: Ensures correct behavior under the specified conditions
- **.id**: Ensures correct behavior under the specified conditions
- **.get**: Ensures correct behavior under the specified conditions
- **.set**: Ensures correct behavior under the specified conditions
- **.remove**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/stories/pinned_articles_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/pinned_article.rb` -- data persistence, validations, and associations
- **Policy layer**: `app/policies/pinned_article_policy.rb` -- authorization and access control rules
- **Model layer**: `app/models/article.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/cached_entity.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/lever_catalog_builder.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/order_by_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/relevancy_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/variant_assembler.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_article.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/recommended_articles_list.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: returns false if there is no pinned article

- **Given** there is no pinned article
- **When** the action is triggered
- **Then** returns false

### S-2: returns false if the pinned article has been unpublished

- **Given** the pinned article has been unpublished
- **When** the action is triggered
- **Then** returns false

### S-3: returns false if the pinned article has been deleted

- **Given** the pinned article has been deleted
- **When** the action is triggered
- **Then** returns false

### S-4: returns true if there is a pinned article

- **Given** there is a pinned article
- **When** the action is triggered
- **Then** returns true

### S-5: returns nil if there is no pinned article

- **Given** there is no pinned article
- **When** the action is triggered
- **Then** returns nil

### S-6: returns nil if the pinned article has been unpublished

- **Given** the pinned article has been unpublished
- **When** the action is triggered
- **Then** returns nil

### S-7: returns nil if the pinned article has been deleted

- **Given** the pinned article has been deleted
- **When** the action is triggered
- **Then** returns nil

### S-8: returns the id of the pinned article

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the id of the pinned article

### S-9: returns nil if there is no pinned article

- **Given** there is no pinned article
- **When** the action is triggered
- **Then** returns nil

### S-10: returns nil if the pinned article has been unpublished

- **Given** the pinned article has been unpublished
- **When** the action is triggered
- **Then** returns nil

### S-11: returns nil if the pinned article has been deleted

- **Given** the pinned article has been deleted
- **When** the action is triggered
- **Then** returns nil

### S-12: returns the pinned article

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the pinned article

