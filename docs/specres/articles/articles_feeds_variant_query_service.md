---
id: "01KHY7PZHHKAF0S5KAPQY2AC3F"
name: "articles_feeds_variant_query_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/articles/feeds/variant_query.rb
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
- spec/services/articles/feeds/variant_query_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::Feeds::VariantQuery` within the articles domain.

### Behavioral Areas

- **.build_for with #{variant} variant**: does return article published 27 hours before last page view if last comment is within 6 hours
- **call with nil user**: does return article published 27 hours before last page view if last comment is within 6 hours
- **call with a non-nil user**: does return article published 27 hours before last page view if last comment is within 6 hours
- **featured_story_and_default_home_feed**: Ensures correct behavior under the specified conditions
- **.build_for with broken #{variant} variant**: does return article published 27 hours before last page view if last comment is within 6 hours
- **with a non-nil user**: does return article published 27 hours before last page view if last comment is within 6 hours
- **with a nil user**: does return article published 27 hours before last page view if last comment is within 6 hours

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/articles/feeds/variant_query.rb` -- business logic orchestration and domain operations
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

### S-1: is a valid ActiveRecord::Relation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is a valid ActiveRecord::Relation

### S-2: is a valid ActiveRecord::Relation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is a valid ActiveRecord::Relation

### S-3: does not return negative scored articles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not return negative scored articles

### S-4: does not return an article published 27 hours before last page view if last comm...

- **Given** last comment at is too old
- **When** the action is triggered
- **Then** does not return an article published 27 hours before last page view

### S-5: does return article published 27 hours before last page view if last comment is ...

- **Given** last comment is within 6 hours
- **When** the action is triggered
- **Then** does return article published 27 hours before last page view

### S-6: does not return article published 38 hours before last page view if last comment...

- **Given** last comment is within 6 hours
- **When** the action is triggered
- **Then** does not return article published 38 hours before last page view

### S-7: returns proper scope when passed the different test values

- **Given** the system is in a standard operational state
- **When** passed the different test values
- **Then** returns proper scope

### S-8: returns an array with two elements and entries

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an array with two elements and entries

