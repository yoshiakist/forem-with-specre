---
id: "01KHY7PZPPBSAYGN2QGR9B9ZDY"
name: "comments_tree_query"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/queries/comments/tree.rb
- app/controllers/admin/comments_controller.rb
- app/controllers/api/v0/comments_controller.rb
- app/controllers/api/v1/comments_controller.rb
- app/controllers/comments_controller.rb
- app/controllers/concerns/api/comments_controller.rb
- app/helpers/comments_helper.rb
- app/queries/comments/community_wellness_query.rb
- app/queries/comments/count.rb
- app/services/comments/calculate_score.rb
- app/services/exporter/comments.rb
- spec/queries/comments/tree_spec.rb

## Functional Overview

This specification defines the expected behavior of `Comments::Tree` within the comments domain.

### Behavioral Areas

- **for_commentable**: Ensures correct behavior under the specified conditions
- **with include_negative**: returns comments with low score if include_negative is passed
- **with sort order**: returns comments with low score if include_negative is passed
- **for_root_comment**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Query object**: `app/queries/comments/tree.rb` -- complex database query encapsulation
- **Controller layer**: `app/controllers/admin/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/comments_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/comments_helper.rb` -- shared view utility methods
- **Query object**: `app/queries/comments/community_wellness_query.rb` -- complex database query encapsulation
- **Query object**: `app/queries/comments/count.rb` -- complex database query encapsulation
- **Service layer**: `app/services/comments/calculate_score.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/exporter/comments.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns a full tree

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a full tree

### S-2: returns part of the tree

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns part of the tree

### S-3: returns comments with low score if include_negative is passed

- **Given** include_negative is passed
- **When** the action is triggered
- **Then** returns comments with low score

### S-4: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-5: returns comments in the right order when order is oldest

- **Given** the system is in a standard operational state
- **When** order is oldest
- **Then** returns comments in the right order

### S-6: returns comments in the right order when order is latest

- **Given** the system is in a standard operational state
- **When** order is latest
- **Then** returns comments in the right order

### S-7: returns comments in the right order when order is top

- **Given** the system is in a standard operational state
- **When** order is top
- **Then** returns comments in the right order

### S-8: returns tree for a particular comment

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns tree for a particular comment

### S-9: returns tree with negative comments

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns tree with negative comments

