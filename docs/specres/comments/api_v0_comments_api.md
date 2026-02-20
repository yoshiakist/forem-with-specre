---
id: "01KHY7PZPSA4PTJ7R859571SJ1"
name: "api_v0_comments_api"
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
- spec/requests/api/v0/comments_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Api::V0::Comments"` within the comments domain.

### Behavioral Areas

- **Api::V0::Comments**: Ensures correct behavior under the specified conditions
- **GET /api/comments**: Ensures correct behavior under the specified conditions
- **when a comment is deleted**: returns comments for article
- **when a comment is hidden**: returns comments for article
- **when getting by podcast episode id**: not found if bad podcast episode id
- **GET /api/comments/:id**: Ensures correct behavior under the specified conditions
- **when a comment is deleted**: returns comments for article
- **when a comment is hidden**: returns comments for article

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

### S-1: returns not found if wrong article id

- **Given** wrong article id
- **When** the action is triggered
- **Then** returns not found

### S-2: returns comments for article

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns comments for article

### S-3: does not include children comments in the root list

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not include children comments in the root list

### S-4: includes children comments in the children list

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes children comments in the children list

### S-5: includes grandchildren comments in the children-children list

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes grandchildren comments in the children-children list

### S-6: includes great-grandchildren comments in the children-children-children list

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes great-grandchildren comments in the children-children-children list

### S-7: sets the correct edge caching surrogate key for all the comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the correct edge caching surrogate key for all the comments

### S-8: returns date created

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns date created

### S-9: appears in the thread

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** appears in the thread

### S-10: replaces the body_html

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** replaces the body_html

### S-11: does not render the user information

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not render the user information

### S-12: still has children comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** still has children comments

