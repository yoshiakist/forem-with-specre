---
id: "01KHY7PZNHSRYSV2RSQ4QQECHK"
name: "moderator_sink_articles_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/moderator/sink_articles_worker.rb
- app/services/moderator/sink_articles.rb
- app/services/moderator/unpublish_all_articles.rb
- app/workers/moderator/unpublish_all_articles_worker.rb
- spec/workers/moderator/sink_articles_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Moderator::SinkArticlesWorker` within the articles domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/moderator/sink_articles_worker.rb` -- asynchronous job processing
- **Service layer**: `app/services/moderator/sink_articles.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/moderator/unpublish_all_articles.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/moderator/unpublish_all_articles_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: returns early when user not found

- **Given** the system is in a standard operational state
- **When** user not found
- **Then** returns early

### S-2: updates score for user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates score for user

### S-3: skips draft articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** skips draft articles

