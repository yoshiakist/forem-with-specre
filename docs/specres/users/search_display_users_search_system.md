---
id: "01KHY7Q02FN9BT8VP8XT2WTGFB"
name: "search_display_users_search_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/concerns/algolia_searchable/searchable_user.rb
- app/serializers/search/nested_user_serializer.rb
- app/serializers/search/simple_user_serializer.rb
- app/serializers/search/user_serializer.rb
- app/services/search/user.rb
- app/services/search/username.rb
- spec/system/search/display_users_search_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Display` within the users domain.

### Behavioral Areas

- **Display users search spec**: returns correct results for name search

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/concerns/algolia_searchable/searchable_user.rb` -- data persistence, validations, and associations
- **Serializer**: `app/serializers/search/nested_user_serializer.rb` -- API response formatting and data transformation
- **Serializer**: `app/serializers/search/simple_user_serializer.rb` -- API response formatting and data transformation
- **Serializer**: `app/serializers/search/user_serializer.rb` -- API response formatting and data transformation
- **Service layer**: `app/services/search/user.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/search/username.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns correct results for name search

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns correct results for name search

### S-2: /search?q=jane&filters=class_name:User

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /search?q=jane&filters=class_name:User

### S-3: returns all expected user fields

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns all expected user fields

### S-4: /search?q=jane&filters=class_name:User

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /search?q=jane&filters=class_name:User

