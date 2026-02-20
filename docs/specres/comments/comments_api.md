---
id: "01KHY7PZQ4E3G8ZV2R3DTH636P"
name: "comments_api"
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
- spec/requests/comments_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Comments"` within the comments domain.

### Behavioral Areas

- **Comments**: displays all comments except for below -400 score for signed in
- **GET comment index**: displays a comment
- **when there are comments with different score**: displays all comments except for below -400 score for signed in
- **when there are child spam comments**: displays all comments except for below -400 score for signed in
- **when the comment is a root**: displays a comment
- **when the comment is a child comment**: displays a comment
- **when the comment is two levels nested and hidden**: displays a comment
- **when the comment is a sibling of a child comment and is hidden**: displays a comment

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

### S-1: returns 200

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns 200

### S-2: displays a comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays a comment

### S-3: displays all comments except for below -400 score for signed in

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays all comments except for below -400 score for signed in

### S-4: displays deleted message and children of a spam comment for signed in

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays deleted message and children of a spam comment for signed in

### S-5: displays only comments with positive score for signed out user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** displays only comments with positive score for signed out user

### S-6: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-7: hides child spam comment if it has no children

- **Given** it has no children
- **When** the action is triggered
- **Then** hides child spam comment

### S-8: displays the comment hidden message if the comment is hidden

- **Given** the comment is hidden
- **When** the action is triggered
- **Then** displays the comment hidden message

### S-9: displays the comment anyway if it is hidden

- **Given** it is hidden
- **When** the action is triggered
- **Then** displays the comment anyway

### S-10: displays noindex if comment has score of less than 0

- **Given** comment has score of less than 0
- **When** the action is triggered
- **Then** displays noindex

### S-11: does not display noindex if comment has 0 or more score

- **Given** comment has 0 or more score
- **When** the action is triggered
- **Then** does not display noindex

### S-12: displays noindex if commentable has score of less than 0

- **Given** commentable has score of less than 0
- **When** the action is triggered
- **Then** displays noindex

