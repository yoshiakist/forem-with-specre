---
id: "01KHY7PZQQ3FV5WBVWX2GFTX7A"
name: "comment_creator_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/comment_creator.rb
- app/services/ai/comment_check.rb
- app/services/ai/comment_helpfulness_assessor.rb
- app/services/badges/award_beloved_comment.rb
- app/services/comments/calculate_score.rb
- app/services/edge_cache/bust_comment.rb
- app/services/exporter/comments.rb
- app/services/markdown_processor/fixer/fix_for_comment.rb
- app/services/notifications/new_comment/send.rb
- app/services/search/comment.rb
- app/services/slack/messengers/comment_user_warned.rb
- spec/services/comment_creator_spec.rb

## Functional Overview

This specification defines the expected behavior of `CommentCreator` within the comments domain.

### Behavioral Areas

- **when save is successful**: Ensures correct behavior under the specified conditions
- **when save is unsuccessful**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/comment_creator.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/comment_check.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/ai/comment_helpfulness_assessor.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/badges/award_beloved_comment.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/comments/calculate_score.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/edge_cache/bust_comment.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/exporter/comments.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/markdown_processor/fixer/fix_for_comment.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/new_comment/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/search/comment.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/slack/messengers/comment_user_warned.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: responds as if Comment

- **Given** Comment
- **When** the action is triggered
- **Then** responds as

### S-2: notifies subscribers

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** notifies subscribers

### S-3: creates a new reaction

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new reaction

### S-4: does not notify subscribers

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not notify subscribers

### S-5: does not create a new reaction

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not create a new reaction

