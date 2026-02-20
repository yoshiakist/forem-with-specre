---
id: "01KHY7PZJSV0X91W328KRERC4B"
name: "moderator_sink_articles_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/moderator/sink_articles.rb
- app/workers/moderator/sink_articles_worker.rb
- app/services/moderator/unpublish_all_articles.rb
- app/workers/moderator/unpublish_all_articles_worker.rb
- spec/services/moderator/sink_articles_spec.rb

## Functional Overview

This specification defines the expected behavior of `Moderator::SinkArticles` within the articles domain.

### Behavioral Areas

- **call**: Ensures correct behavior under the specified conditions
- **when removing a user vomit reaction**: lowers all of a user

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/moderator/sink_articles.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/moderator/sink_articles_worker.rb` -- asynchronous job processing
- **Service layer**: `app/services/moderator/unpublish_all_articles.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/moderator/unpublish_all_articles_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: lowers all of a user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** lowers all of a user

### S-2: lowers all of the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** lowers all of the user

### S-3: raises all of the user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises all of the user

