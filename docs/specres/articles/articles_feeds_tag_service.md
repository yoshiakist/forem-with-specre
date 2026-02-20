---
id: "01KHY7PZHCYHMS6DT8STQSP77B"
name: "articles_feeds_tag_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/stories/tagged_articles_controller.rb
- app/services/articles/feeds/tag.rb
- app/models/articles/feeds.rb
- app/models/articles/feeds/lever_catalog_builder.rb
- app/models/articles/feeds/order_by_lever.rb
- app/models/articles/feeds/relevancy_lever.rb
- app/models/articles/feeds/variant_assembler.rb
- app/services/articles/feeds/article_score_calculator_for_user.rb
- app/services/articles/feeds/basic.rb
- app/services/articles/feeds/custom.rb
- app/services/articles/feeds/find_featured_story.rb
- app/services/articles/feeds/large_forem_experimental.rb
- spec/services/articles/feeds/tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::Feeds::Tag` within the articles domain.

### Behavioral Areas

- **with tag**: returns articles with the specified tag

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/stories/tagged_articles_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/articles/feeds/tag.rb` -- business logic orchestration and domain operations
- **Model layer**: `app/models/articles/feeds.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/lever_catalog_builder.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/order_by_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/relevancy_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/variant_assembler.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/articles/feeds/article_score_calculator_for_user.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/basic.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/custom.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/find_featured_story.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/large_forem_experimental.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns published articles only

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns published articles only

### S-2: returns articles with the specified tag

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns articles with the specified tag

