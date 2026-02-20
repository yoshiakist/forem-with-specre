---
id: "01KHY7PZJVK0J1XDGX0C9V4TRF"
name: "moderator_unpublish_all_articles_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/moderator/unpublish_all_articles.rb
- app/workers/moderator/unpublish_all_articles_worker.rb
- app/services/moderator/sink_articles.rb
- app/workers/moderator/sink_articles_worker.rb
- spec/services/moderator/unpublish_all_articles_spec.rb

## Functional Overview

This specification defines the expected behavior of `Moderator::UnpublishAllArticles` within the articles domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/moderator/unpublish_all_articles.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/moderator/unpublish_all_articles_worker.rb` -- asynchronous job processing
- **Service layer**: `app/services/moderator/sink_articles.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/moderator/sink_articles_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: unpublishes all articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** unpublishes all articles

### S-2: unpublishes related comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** unpublishes related comments

### S-3: applies proper frontmatter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** applies proper frontmatter

### S-4: destroys the pre-existing notifications

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** destroys the pre-existing notifications

### S-5: destroys the pre-existing context notifications

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** destroys the pre-existing context notifications

### S-6: creates audit_log records

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates audit_log records

### S-7: creates audit_log records for admin action

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates audit_log records for admin action

