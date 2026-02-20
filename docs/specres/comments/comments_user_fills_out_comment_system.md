---
id: "01KHY7PZRN5QQEW04CY4GY4KYN"
name: "comments_user_fills_out_comment_system"
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
- spec/system/comments/user_fills_out_comment_spec.rb

## Functional Overview

This specification defines the expected behavior of `User_Fills_Out_Comment` within the comments domain.

### Behavioral Areas

- **Creating Comment**: User fills out comment box normally
- **with runkit_tag**: closes modal with close button
- **when user makes too many comments**: User fills out comment box normally
- **when there is an error posting a comment**: User fills out comment box normally
- **with Runkit tags**: closes modal with close button
- **with TwitterTimeline tag**: closes modal with close button

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

### S-1: User fills out comment box normally

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** User fills out comment box normally

### S-2: displays a rate limit modal

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays a rate limit modal

### S-3: closes modal with close button

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** closes modal with close button

### S-4: closes model with 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** closes model with 

### S-5: displays a error modal

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays a error modal

### S-6: Users fills out comment box with a Runkit tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** Users fills out comment box with a Runkit tag

### S-7: Users fills out comment box 2 Runkit tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** Users fills out comment box 2 Runkit tags

### S-8: User fill out comment box with a Runkit tag, then clicks preview

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** User fill out comment box with a Runkit tag, then clicks preview

### S-9: User fill out comment box with a TwitterTimeline tag, then clicks preview

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** User fill out comment box with a TwitterTimeline tag, then clicks preview

### S-10: User fill out comment box then click previews and submit

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** User fill out comment box then click previews and submit

### S-11: User replies to a comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** User replies to a comment

### S-12: User attaches a valid image

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** User attaches a valid image

