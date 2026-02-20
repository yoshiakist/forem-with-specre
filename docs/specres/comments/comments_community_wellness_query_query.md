---
id: "01KHY7PZPHMRZ0K1XXAWZSQX0C"
name: "comments_community_wellness_query_query"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/queries/comments/community_wellness_query.rb
- app/controllers/admin/comments_controller.rb
- app/controllers/api/v0/comments_controller.rb
- app/controllers/api/v1/comments_controller.rb
- app/controllers/comments_controller.rb
- app/controllers/concerns/api/comments_controller.rb
- app/helpers/comments_helper.rb
- app/queries/comments/count.rb
- app/queries/comments/tree.rb
- app/services/comments/calculate_score.rb
- app/services/exporter/comments.rb
- spec/queries/comments/community_wellness_query_spec.rb

## Functional Overview

This specification defines the expected behavior of `Comments::CommunityWellnessQuery` within the comments domain.

### Behavioral Areas

- **when multiple users match criteria**: returns users with correct data on their corresponding hash
- **when users match criteria but mod reaction reduces their comment counts**: returns users with correct data on their corresponding hash

### Implementation Architecture

The behavior is implemented across the following layers:

- **Query object**: `app/queries/comments/community_wellness_query.rb` -- complex database query encapsulation
- **Controller layer**: `app/controllers/admin/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/comments_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/comments_helper.rb` -- shared view utility methods
- **Query object**: `app/queries/comments/count.rb` -- complex database query encapsulation
- **Query object**: `app/queries/comments/tree.rb` -- complex database query encapsulation
- **Service layer**: `app/services/comments/calculate_score.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/exporter/comments.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns the correct data structure (array of hashes w/ correct keys)

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct data structure (array of hashes w/ correct keys)

### S-2: returns users with correct data on their corresponding hash

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns users with correct data on their corresponding hash

### S-3: matches the correct comment count for each week in result hash

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** matches the correct comment count for each week in result hash

