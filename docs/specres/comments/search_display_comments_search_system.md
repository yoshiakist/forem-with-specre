---
id: "01KHY7PZRV6VVA5ZBD9QWHSTEQ"
name: "search_display_comments_search_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/concerns/algolia_searchable/searchable_comment.rb
- app/serializers/search/comment_serializer.rb
- app/services/search/comment.rb
- spec/system/search/display_comments_search_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Display` within the comments domain.

### Behavioral Areas

- **Display articles search spec**: returns correct results for a search

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/concerns/algolia_searchable/searchable_comment.rb` -- data persistence, validations, and associations
- **Serializer**: `app/serializers/search/comment_serializer.rb` -- API response formatting and data transformation
- **Service layer**: `app/services/search/comment.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns correct results for a search

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns correct results for a search

### S-2: /search?q=#{url_encoded_query}&filters=class_name:Comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /search?q=#{url_encoded_query}&filters=class_name:Comment

