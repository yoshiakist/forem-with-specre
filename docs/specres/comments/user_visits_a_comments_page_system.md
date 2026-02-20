---
id: "01KHY7PZS0EADXQJH918PWJBNR"
name: "user_visits_a_comments_page_system"
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
- spec/system/user_visits_a_comments_page_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Views` within the comments domain.

### Behavioral Areas

- **Views an article**: #{article.path}/comments

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/discussion_locks_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: shows all comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows all comments

### S-2: #{article.path}/comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** #{article.path}/comments

### S-3: shows op marker on author and co-author comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows op marker on author and co-author comments

### S-4: #{article.path}/comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** #{article.path}/comments

### S-5: shows special op marker on ama articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows special op marker on ama articles

### S-6: #{ama_article.path}/comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** #{ama_article.path}/comments

### S-7: shows a thread

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows a thread

### S-8: #{article.path}/comments/#{comment.id_code_generated}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** #{article.path}/comments/#{comment.id_code_generated}

