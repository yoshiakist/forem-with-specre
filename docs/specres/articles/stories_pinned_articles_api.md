---
id: "01KHY7PZFXZ8XA1M3N8G0ZVVWV"
name: "stories_pinned_articles_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/stories/pinned_articles_controller.rb
- app/controllers/stories/articles_search_controller.rb
- app/controllers/stories/tagged_articles_controller.rb
- spec/requests/stories/pinned_articles_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Stories::PinnedArticlesController"` within the articles domain.

### Behavioral Areas

- **Stories::PinnedArticlesController**: Ensures correct behavior under the specified conditions
- **show**: Ensures correct behavior under the specified conditions
- **when unauthorized**: rejects a requested by an unauthorized user
- **when authorized**: rejects a requested by an unauthorized user
- **update**: updates the pinned article
- **when unauthorized**: rejects a requested by an unauthorized user
- **when authorized**: rejects a requested by an unauthorized user
- **destroy**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/stories/pinned_articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/articles_search_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/tagged_articles_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: rejects a requested by an unauthenticated user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects a requested by an unauthenticated user

### S-2: rejects a requested by an unauthorized user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects a requested by an unauthorized user

### S-3: responds with :not_found if there is no pinned article

- **Given** there is no pinned article
- **When** the action is triggered
- **Then** responds with :not_found

### S-4: responds with the expected JSON response

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** responds with the expected JSON response

### S-5: rejects a requested by an unauthenticated user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects a requested by an unauthenticated user

### S-6: rejects a requested by an unauthorized user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects a requested by an unauthorized user

### S-7: responds with :unprocessable_entity if a non integer id is passed

- **Given** a non integer id is passed
- **When** the action is triggered
- **Then** responds with :unprocessable_entity

### S-8: responds with :unprocessable_entity if an invalid article id is passed

- **Given** an invalid article id is passed
- **When** the action is triggered
- **Then** responds with :unprocessable_entity

### S-9: responds with :unprocessable_entity if a draft article id is passed

- **Given** a draft article id is passed
- **When** the action is triggered
- **Then** responds with :unprocessable_entity

### S-10: responds with :no_content if a valid article id is passed

- **Given** a valid article id is passed
- **When** the action is triggered
- **Then** responds with :no_content

### S-11: updates the pinned article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the pinned article

### S-12: creates an audit log

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an audit log

