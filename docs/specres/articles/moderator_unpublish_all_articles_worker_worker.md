---
id: "01KHY7PZNMYTZ3HHH64CWXBR1W"
name: "moderator_unpublish_all_articles_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/moderator/unpublish_all_articles_worker.rb
- app/services/moderator/sink_articles.rb
- app/services/moderator/unpublish_all_articles.rb
- app/workers/moderator/sink_articles_worker.rb
- spec/workers/moderator/unpublish_all_articles_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Moderator::UnpublishAllArticlesWorker` within the articles domain.

### Behavioral Areas

- **when unpublishing**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/moderator/unpublish_all_articles_worker.rb` -- asynchronous job processing
- **Service layer**: `app/services/moderator/sink_articles.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/moderator/unpublish_all_articles.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/moderator/sink_articles_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: calls UnpublishAllArticles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls UnpublishAllArticles

### S-2: calls UnpublishAllArticles with listener

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls UnpublishAllArticles with listener

### S-3: calls UnpublishAllArticles with the default listener

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls UnpublishAllArticles with the default listener

### S-4: calls UnpublishAllArticles with the default listener if passed invalid listener

- **Given** passed invalid listener
- **When** the action is triggered
- **Then** calls UnpublishAllArticles with the default listener

