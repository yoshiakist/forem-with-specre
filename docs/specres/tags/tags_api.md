---
id: "01KHY7Q0C0ADZ4MTYET5GQ3ABG"
name: "tags_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/tags_controller.rb
- app/controllers/api/v0/tags_controller.rb
- app/controllers/api/v1/tags_controller.rb
- app/controllers/concerns/api/tags_controller.rb
- app/controllers/liquid_tags_controller.rb
- app/controllers/tags_controller.rb
- app/workers/tags/resave_supported_tags_worker.rb
- spec/requests/tags_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Tags"` within the tags domain.

### Behavioral Areas

- **Tags**: does not include tags with alias
- **GET /tags**: Ensures correct behavior under the specified conditions
- **GET /tags/bulk**: Ensures correct behavior under the specified conditions
- **GET /tags/suggest**: Ensures correct behavior under the specified conditions
- **GET /t/:tag/edit**: Ensures correct behavior under the specified conditions
- **when user is a tag moderator**: does not allow not logged-in users
- **UPDATE /tags**: allows authorized tag moderators to update a tag
- **when user is a tag moderator**: does not allow not logged-in users

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/liquid_tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/tags_controller.rb` -- HTTP request routing and response handling
- **Background worker**: `app/workers/tags/resave_supported_tags_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: returns proper page

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns proper page

### S-2: does not include tags with alias

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not include tags with alias

### S-3: searches tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** searches tags

### S-4: returns a JSON representation of the top tags

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a JSON representation of the top tags

### S-5: finds tags from array of tag_ids

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** finds tags from array of tag_ids

### S-6: finds tags from array of tag_names

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** finds tags from array of tag_names

### S-7: returns a JSON representation of the top tags

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a JSON representation of the top tags

### S-8: does not allow not logged-in users

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow not logged-in users

### S-9: does not allow users who are not tag moderators

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow users who are not tag moderators

### S-10: allows super admins

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows super admins

### S-11: allows authorized tag moderators

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows authorized tag moderators

### S-12: does not allow moderators of one tag to edit another tag

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow moderators of one tag to edit another tag

