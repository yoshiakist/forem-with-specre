---
id: "01KHY7PZK7JXRMWXE41CAS8TNP"
name: "users_delete_articles_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/users/delete_articles.rb
- app/workers/users/resave_articles_worker.rb
- spec/services/users/delete_articles_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::DeleteArticles` within the articles domain.

### Behavioral Areas

- **with comments**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/users/delete_articles.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/users/resave_articles_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: deletes articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes articles

### S-2: deletes the articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes the articles

### S-3: deletes articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** deletes articles

### S-4: busts cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts cache

