---
id: "01KHY7PZPMWN8TDJ2WB815W1SS"
name: "comments_count_query"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/queries/comments/count.rb
- app/controllers/admin/comments_controller.rb
- app/controllers/api/v0/comments_controller.rb
- app/controllers/api/v1/comments_controller.rb
- app/controllers/comments_controller.rb
- app/controllers/concerns/api/comments_controller.rb
- app/helpers/comments_helper.rb
- app/queries/comments/community_wellness_query.rb
- app/queries/comments/tree.rb
- app/services/comments/calculate_score.rb
- app/services/exporter/comments.rb
- spec/queries/comments/count_spec.rb

## Functional Overview

This specification defines the expected behavior of `Comments::Count` within the comments domain.

### Behavioral Areas

- **with recalculate option**: returns correct number with regular comments

### Implementation Architecture

The behavior is implemented across the following layers:

- **Query object**: `app/queries/comments/count.rb` -- complex database query encapsulation
- **Controller layer**: `app/controllers/admin/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/comments_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/comments_helper.rb` -- shared view utility methods
- **Query object**: `app/queries/comments/community_wellness_query.rb` -- complex database query encapsulation
- **Query object**: `app/queries/comments/tree.rb` -- complex database query encapsulation
- **Service layer**: `app/services/comments/calculate_score.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/exporter/comments.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns correct number with regular comments

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns correct number with regular comments

### S-2: returns correct number with children

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns correct number with children

### S-3: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-4: includes ok children of a low-score comment (but not low-score children)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes ok children of a low-score comment (but not low-score children)

### S-5: includes children of a low-score comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes children of a low-score comment

### S-6: includes a comment with low-score ancestors

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes a comment with low-score ancestors

### S-7: returns displayed_comments_count if it exists + no recalculate

- **Given** it exists + no recalculate
- **When** the action is triggered
- **Then** returns displayed_comments_count

### S-8: recalculates if recalculate is passed

- **Given** recalculate is passed
- **When** the action is triggered
- **Then** recalculates

### S-9: recalculates if no recalculate and no displayed_comments_count

- **Given** no recalculate and no displayed_comments_count
- **When** the action is triggered
- **Then** recalculates

