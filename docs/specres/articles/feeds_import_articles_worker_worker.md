---
id: "01KHY7PZNFNSTMAMXP4Q8MWR0E"
name: "feeds_import_articles_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/feeds/import_articles_worker.rb
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
- spec/workers/feeds/import_articles_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Feeds::ImportArticlesWorker` within the articles domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/feeds/import_articles_worker.rb` -- asynchronous job processing
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

### S-1: processes jobs for users with feeds

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** processes jobs for users with feeds

### S-2: enqueues job for user with the given time

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enqueues job for user with the given time

### S-3: calls Feeds::Import with the users from the given user ids and no time

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls Feeds::Import with the users from the given user ids and no time

