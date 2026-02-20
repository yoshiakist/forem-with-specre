---
id: "01KHY7PZQSGM9AYR0T54VJZM8F"
name: "comments_calculate_score_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/comments/calculate_score.rb
- app/workers/comments/calculate_score_worker.rb
- app/controllers/admin/comments_controller.rb
- app/controllers/api/v0/comments_controller.rb
- app/controllers/api/v1/comments_controller.rb
- app/controllers/comments_controller.rb
- app/controllers/concerns/api/comments_controller.rb
- app/helpers/comments_helper.rb
- app/queries/comments/community_wellness_query.rb
- app/queries/comments/count.rb
- app/queries/comments/tree.rb
- app/services/exporter/comments.rb
- spec/services/comments/calculate_score_spec.rb

## Functional Overview

This specification defines the expected behavior of `Comments::CalculateScore` within the comments domain.

### Behavioral Areas

- **when adding spam role**: updates the score and updated_at with a penalty if the user is a spammer

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/comments/calculate_score.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/comments/calculate_score_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/comments_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/comments_helper.rb` -- shared view utility methods
- **Query object**: `app/queries/comments/community_wellness_query.rb` -- complex database query encapsulation
- **Query object**: `app/queries/comments/count.rb` -- complex database query encapsulation
- **Query object**: `app/queries/comments/tree.rb` -- complex database query encapsulation
- **Service layer**: `app/services/exporter/comments.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: updates the score

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the score

### S-2: updates the score and updated_at with a penalty if the user is a spammer

- **Given** the user is a spammer
- **When** the action is triggered
- **Then** updates the score and updated_at with a penalty

### S-3: updates article displayed comments count

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates article displayed comments count

