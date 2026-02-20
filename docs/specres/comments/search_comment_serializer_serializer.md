---
id: "01KHY7PZQFRAYBTJWPRS7NRT5J"
name: "search_comment_serializer_serializer"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/serializers/search/comment_serializer.rb
- app/models/concerns/algolia_searchable/searchable_comment.rb
- app/services/search/comment.rb
- spec/serializers/search/comment_serializer_spec.rb

## Functional Overview

This specification defines the expected behavior of `Search::CommentSerializer` within the comments domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Serializer**: `app/serializers/search/comment_serializer.rb` -- API response formatting and data transformation
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_comment.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/search/comment.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: serializes a Comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** serializes a Comment

### S-2: serializes the comment path

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** serializes the comment path

### S-3: serializes highlight

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** serializes highlight

### S-4: serializes the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** serializes the user

