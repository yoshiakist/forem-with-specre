---
id: "01KHY7PZD46KYAHY8Q9AVBDY3K"
name: "article_organization_baseline_score_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/article.rb
- app/models/articles/cached_entity.rb
- app/models/articles/feeds.rb
- app/models/articles/feeds/lever_catalog_builder.rb
- app/models/articles/feeds/order_by_lever.rb
- app/models/articles/feeds/relevancy_lever.rb
- app/models/articles/feeds/variant_assembler.rb
- app/models/concerns/algolia_searchable/searchable_article.rb
- app/models/pinned_article.rb
- app/models/recommended_articles_list.rb
- spec/models/article_organization_baseline_score_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Article` within the articles domain.

### Behavioral Areas

- **Article Organization Baseline Score**: adds the organization baseline score to the article score

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/article.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/cached_entity.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/lever_catalog_builder.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/order_by_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/relevancy_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/variant_assembler.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_article.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/pinned_article.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/recommended_articles_list.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: adds the organization baseline score to the article score

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds the organization baseline score to the article score

### S-2: defaults to 0 if organization has no baseline score

- **Given** organization has no baseline score
- **When** the action is triggered
- **Then** defaults to 0

### S-3: does not affect articles without an organization

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not affect articles without an organization

