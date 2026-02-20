---
id: "01KHY7PZQYQ65MXDJYP8RRSHMD"
name: "exporter_comments_service"
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
- app/services/exporter/comments.rb
- app/services/users/delete_comments.rb
- spec/services/exporter/comments_spec.rb

## Functional Overview

This specification defines the expected behavior of `Exporter::Comments` within the comments domain.

### Behavioral Areas

- **initialize**: Ensures correct behavior under the specified conditions
- **export**: Ensures correct behavior under the specified conditions
- **when id code is unknown**: returns no comments if the id code is not found
- **when id code is known**: returns no comments if the id code is not found
- **when all comments are requested**: names itself comments
- **commentable path**: contains the path of the article

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/comments_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/comments_helper.rb` -- shared view utility methods
- **Service layer**: `app/services/exporter/comments.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/delete_comments.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: accepts a user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a user

### S-2: names itself comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** names itself comments

### S-3: returns no comments if the id code is not found

- **Given** the id code is not found
- **When** the action is triggered
- **Then** returns no comments

### S-4: no comments if id code belongs to another user

- **Given** id code belongs to another user
- **When** the action is triggered
- **Then** no comments

### S-5: returns the comment

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the comment

### S-6: returns only expected fields for the comment

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns only expected fields for the comment

### S-7: returns all the comments as json

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns all the comments as json

### S-8: returns only expected fields for the comment

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns only expected fields for the comment

### S-9: contains the path of the article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** contains the path of the article

### S-10: contains the path of the podcast episode

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** contains the path of the podcast episode

