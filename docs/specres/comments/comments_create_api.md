---
id: "01KHY7PZPZHACVN0CSHWSN86EH"
name: "comments_create_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/comments_controller.rb
- app/controllers/api/v0/comments_controller.rb
- app/controllers/api/v1/comments_controller.rb
- app/controllers/comments_controller.rb
- app/controllers/concerns/api/comments_controller.rb
- app/controllers/discussion_locks_controller.rb
- spec/requests/comments_create_spec.rb

## Functional Overview

This specification defines the expected behavior of `"CommentsCreate"` within the comments domain.

### Behavioral Areas

- **CommentsCreate**: Ensures correct behavior under the specified conditions
- **when users hit their rate limits**: returns 429 Too Many Requests when a user reaches their rate limit
- **when user is posting on an author that blocks user**: returns 429 Too Many Requests when a user reaches their rate limit
- **when user is posting on an author that does not block user, but the user has been blocked elsewhere**: returns 429 Too Many Requests when a user reaches their rate limit
- **when user is commenting on a comment by an author who has blocked the user**: creates a comment with proper params
- **when an error is raised before authorization is performed**: returns 429 Too Many Requests when a user reaches their rate limit
- **when a comment is invalid**: creates a comment with proper params
- **when there**: returns 429 Too Many Requests when a user reaches their rate limit

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/discussion_locks_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: creates a comment with proper params

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a comment with proper params

### S-2: creates NotificationSubscription for comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates NotificationSubscription for comment

### S-3: returns 429 Too Many Requests when a user reaches their rate limit

- **Given** the system is in a standard operational state
- **When** a user reaches their rate limit
- **Then** returns 429 Too Many Requests

### S-4: returns 429 Too Many Requests when a new user reaches their rate limit

- **Given** the system is in a standard operational state
- **When** a new user reaches their rate limit
- **Then** returns 429 Too Many Requests

### S-5: returns unauthorized

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns unauthorized

### S-6: creates the new comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates the new comment

### S-7: raises a ModerationUnauthorizedError to prevent the comment from saving

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises a ModerationUnauthorizedError to prevent the comment from saving

### S-8: raises the error when the commenter is downthread of the blocker

- **Given** the system is in a standard operational state
- **When** the commenter is downthread of the blocker
- **Then** raises the error

### S-9: returns an unprocessable_entity response code

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an unprocessable_entity response code

### S-10: returns the proper JSON response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the proper JSON response

### S-11: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-12: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

