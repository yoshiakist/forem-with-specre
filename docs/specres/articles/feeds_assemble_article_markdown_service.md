---
id: "01KHY7PZJEQ3RP3N563BE5WWJF"
name: "feeds_assemble_article_markdown_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/feeds/assemble_article_markdown.rb
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
- spec/services/feeds/assemble_article_markdown_spec.rb

## Functional Overview

This specification defines the expected behavior of `Feeds::AssembleArticleMarkdown` within the articles domain.

### Behavioral Areas

- **when item has a long title**: limits the title to 128 characters by truncation

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/feeds/assemble_article_markdown.rb` -- business logic orchestration and domain operations
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

### S-1: creates markdown head matter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates markdown head matter

### S-2: includes the content from the feed

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes the content from the feed

### S-3: limits the title to 128 characters by truncation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** limits the title to 128 characters by truncation

