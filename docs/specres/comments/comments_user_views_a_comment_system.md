---
id: "01KHY7PZRRPRDK1281VCY9DGNR"
name: "comments_user_views_a_comment_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/comments_controller.rb
- app/controllers/api/v0/comments_controller.rb
- app/controllers/api/v1/comments_controller.rb
- app/controllers/comments_controller.rb
- app/controllers/concerns/api/comments_controller.rb
- app/helpers/comments_helper.rb
- app/queries/comments/community_wellness_query.rb
- app/queries/comments/count.rb
- app/queries/comments/tree.rb
- app/services/comments/calculate_score.rb
- spec/system/comments/user_views_a_comment_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Viewing` within the comments domain.

### Behavioral Areas

- **Viewing a comment**: Ensures correct behavior under the specified conditions
- **when viewing the comment date**: contains a time tag with the correct value for the datetime attribute
- **when a year has passed**: Ensures correct behavior under the specified conditions
- **when the comment is edited and a year has passed**: shows the edited date in the correct format

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/comments_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/comments_helper.rb` -- shared view utility methods
- **Query object**: `app/queries/comments/community_wellness_query.rb` -- complex database query encapsulation
- **Query object**: `app/queries/comments/count.rb` -- complex database query encapsulation
- **Query object**: `app/queries/comments/tree.rb` -- complex database query encapsulation
- **Service layer**: `app/services/comments/calculate_score.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: contains a time tag with the correct value for the datetime attribute

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** contains a time tag with the correct value for the datetime attribute

### S-2: shows the published date in the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the published date in the user

### S-3: shows the published date in the correct format

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the published date in the correct format

### S-4: shows the edited date in the correct format

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the edited date in the correct format

