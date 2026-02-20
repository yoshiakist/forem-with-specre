---
id: "01KHY7PZREFX91XFMPGJWVTAFK"
name: "comments_like_button_state_after_reply_system"
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
- spec/system/comments/like_button_state_after_reply_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Like` within the comments domain.

### Behavioral Areas

- **Like button and tooltip after replying**: keeps the like footer visible and clears replying state on parent after submitting a reply

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

### S-1: keeps the like footer visible and clears replying state on parent after submitti...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** keeps the like footer visible and clears replying state on parent after submitting a reply

