---
id: "01KHY7PZQC2AWTSBJ5RGYQ8QJF"
name: "discussion_locks_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/discussion_locks_controller.rb
- spec/requests/discussion_locks_spec.rb

## Functional Overview

This specification defines the expected behavior of `"DiscussionLocks"` within the comments domain.

### Behavioral Areas

- **DiscussionLocks**: Ensures correct behavior under the specified conditions
- **POST /discussion_locks - DiscussionLocks#create**: Ensures correct behavior under the specified conditions
- **DELETE /discussion_locks/:id - DiscussionLocks#destroy**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/discussion_locks_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: creates a DiscussionLock

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a DiscussionLock

### S-2: returns an error for an Article that already has a DiscussionLock

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an error for an Article that already has a DiscussionLock

### S-3: busts the cache for the article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts the cache for the article

### S-4: does not allow to lock another user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow to lock another user

### S-5: destroys a DiscussionLock

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** destroys a DiscussionLock

### S-6: busts the cache for the article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** busts the cache for the article

