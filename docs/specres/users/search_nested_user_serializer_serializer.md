---
id: "01KHY7PZXGCD0344J7BG3Z91RJ"
name: "search_nested_user_serializer_serializer"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/serializers/search/nested_user_serializer.rb
- app/models/concerns/algolia_searchable/searchable_user.rb
- app/serializers/search/simple_user_serializer.rb
- app/serializers/search/user_serializer.rb
- app/services/search/user.rb
- app/services/search/username.rb
- spec/serializers/search/nested_user_serializer_spec.rb

## Functional Overview

This specification defines the expected behavior of `Search::NestedUserSerializer` within the users domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Serializer**: `app/serializers/search/nested_user_serializer.rb` -- API response formatting and data transformation
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_user.rb` -- data persistence, validations, and associations
- **Serializer**: `app/serializers/search/simple_user_serializer.rb` -- API response formatting and data transformation
- **Serializer**: `app/serializers/search/user_serializer.rb` -- API response formatting and data transformation
- **Service layer**: `app/services/search/user.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/search/username.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: serializes a User

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** serializes a User

