---
id: "01KHY7PZRX297ERMQC2SS322GC"
name: "user_view_user_comments_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/slack/messengers/comment_user_warned.rb
- app/services/users/delete_comments.rb
- spec/system/user/view_user_comments_spec.rb

## Functional Overview

This specification defines the expected behavior of `"User` within the comments domain.

### Behavioral Areas

- **User comments**: /user3000/comments
- **when user is authorized**: /user3000/comments
- **when user is unauthorized**: /user3000/comments
- **when user has too many comments**: /user3000/comments

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/slack/messengers/comment_user_warned.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/delete_comments.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: /user3000/comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /user3000/comments

### S-2: does not show user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not show user

### S-3: shows user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows user

### S-4: hides comments locked cta

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** hides comments locked cta

### S-5: /user3000/comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /user3000/comments

### S-6: does not show user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not show user

### S-7: hides user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** hides user

### S-8: shows comments locked cta

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows comments locked cta

### S-9: /user3000/comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /user3000/comments

### S-10: show user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** show user

### S-11: /user3000/comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /user3000/comments

