---
id: "01KHY7Q0N45758S1F2YXJW3V2N"
name: "moderator_manage_activity_and_roles_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/moderator/manage_activity_and_roles.rb
- app/controllers/admin/moderator_actions_controller.rb
- app/controllers/admin/subforem_moderators/moderators_controller.rb
- app/controllers/admin/tags/moderators_controller.rb
- app/models/moderator_action.rb
- app/queries/admin/moderators_query.rb
- app/queries/users/select_moderators_query.rb
- app/services/moderator/banish_user.rb
- app/services/moderator/delete_user.rb
- app/services/moderator/merge_user.rb
- app/services/moderator/sink_articles.rb
- spec/services/moderator/manage_activity_and_roles_spec.rb

## Functional Overview

This specification defines the expected behavior of `Moderator::ManageActivityAndRoles` within the moderation domain.

### Behavioral Areas

- **when user is in limited role**: adding #{status} also removes the limited role
- **when user is in suspended role**: adding #{status} also removes the limited role
- **when user is in warned role**: adding #{status} also removes the limited role
- **when user is in spam role**: adding #{status} also removes the limited role
- **when user is in comment_suspended role**: adding #{status} also removes the limited role
- **when user is in trusted role**: adding #{status} also removes the limited role
- **when user is in tag_moderator role**: adding #{status} also removes the limited role
- **when user is in admin role**: adding #{status} also removes the limited role

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/moderator/manage_activity_and_roles.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/admin/moderator_actions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/subforem_moderators/moderators_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/tags/moderators_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/moderator_action.rb` -- data persistence, validations, and associations
- **Query object**: `app/queries/admin/moderators_query.rb` -- complex database query encapsulation
- **Query object**: `app/queries/users/select_moderators_query.rb` -- complex database query encapsulation
- **Service layer**: `app/services/moderator/banish_user.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/moderator/delete_user.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/moderator/merge_user.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/moderator/sink_articles.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: adding #{status} also removes the limited role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adding #{status} also removes the limited role

### S-2: adding #{status} also removes the suspended role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adding #{status} also removes the suspended role

### S-3: adding #{status} also removes the warned role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adding #{status} also removes the warned role

### S-4: adding #{status} also removes the spam role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adding #{status} also removes the spam role

### S-5: adding #{status} also removes the comment_suspended role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adding #{status} also removes the comment_suspended role

### S-6: adding #{status} removes the trusted role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adding #{status} removes the trusted role

### S-7: adding #{status} removes the tag_moderator role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adding #{status} removes the tag_moderator role

### S-8: adding #{status} ignores the admin role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adding #{status} ignores the admin role

### S-9: adding #{status} ignores the super_moderator role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adding #{status} ignores the super_moderator role

### S-10: adding #{status} ignores the tech_admin role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adding #{status} ignores the tech_admin role

### S-11: adding #{status} ignores the limited role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adding #{status} ignores the limited role

### S-12: adding #{status} ignores the warned role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adding #{status} ignores the warned role

