---
id: "01KHY7PZGWYDQYWJ0028F7HJWG"
name: "articles_feeds_article_score_calculator_for_user_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/articles/feeds/article_score_calculator_for_user.rb
- app/models/articles/feeds.rb
- app/models/articles/feeds/lever_catalog_builder.rb
- app/models/articles/feeds/order_by_lever.rb
- app/models/articles/feeds/relevancy_lever.rb
- app/models/articles/feeds/variant_assembler.rb
- app/services/articles/feeds/basic.rb
- app/services/articles/feeds/custom.rb
- app/services/articles/feeds/find_featured_story.rb
- app/services/articles/feeds/large_forem_experimental.rb
- app/services/articles/feeds/latest.rb
- spec/services/articles/feeds/article_score_calculator_for_user_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::Feeds::ArticleScoreCalculatorForUser` within the articles domain.

### Behavioral Areas

- **score_followed_user**: Ensures correct behavior under the specified conditions
- **when article is written by a followed user**: returns the followed tag point value
- **when article is not written by a followed user**: returns the followed tag point value
- **score_followed_organization**: Ensures correct behavior under the specified conditions
- **when article is from a followed organization**: returns the followed tag point value
- **when article is not from a followed organization**: returns the followed tag point value
- **when article has no organization**: returns negative of (absolute value of the difference between article and user experience) divided by 2
- **score_followed_tags**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/articles/feeds/article_score_calculator_for_user.rb` -- business logic orchestration and domain operations
- **Model layer**: `app/models/articles/feeds.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/lever_catalog_builder.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/order_by_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/relevancy_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/variant_assembler.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/articles/feeds/basic.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/custom.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/find_featured_story.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/large_forem_experimental.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/latest.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns a score of 1

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a score of 1

### S-2: returns a score of 0

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a score of 0

### S-3: returns a score of 1

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a score of 1

### S-4: returns a score of 0

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a score of 0

### S-5: returns a score of 0

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a score of 0

### S-6: returns the followed tag point value

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the followed tag point value

### S-7: returns the sum of followed tag point values

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the sum of followed tag point values

### S-8: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-9: returns 0

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns 0

### S-10: returns 0

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns 0

### S-11: returns negative of (absolute value of the difference between article and user e...

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns negative of (absolute value of the difference between article and user experience) divided by 2

### S-12: returns proper negative when fractional

- **Given** the system is in a standard operational state
- **When** fractional
- **Then** returns proper negative

