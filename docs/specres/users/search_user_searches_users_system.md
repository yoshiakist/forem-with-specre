---
id: "01KHY7Q02J13QMAH08JZZ97H8V"
name: "search_user_searches_users_system"
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
- spec/system/search/user_searches_users_spec.rb

## Functional Overview

This specification defines the expected behavior of `"User` within the users domain.

### Behavioral Areas

- **User searches users**: /search?q=&filters=class_name:User

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/concerns/algolia_searchable/searchable_user.rb` -- data persistence, validations, and associations
- **Serializer**: `app/serializers/search/nested_user_serializer.rb` -- API response formatting and data transformation
- **Serializer**: `app/serializers/search/simple_user_serializer.rb` -- API response formatting and data transformation
- **Serializer**: `app/serializers/search/user_serializer.rb` -- API response formatting and data transformation
- **Service layer**: `app/services/search/user.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/search/username.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: shows the correct follow buttons

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the correct follow buttons

### S-2: /search?q=&filters=class_name:User

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /search?q=&filters=class_name:User

