---
id: "01KHY7Q0NJ0J8FQ1040NXFRYP9"
name: "subforem_moderators_remove_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/notifications/remove_by_spammer.rb
- app/services/subforem_moderators/remove.rb
- app/services/tag_moderators/remove.rb
- app/workers/notifications/remove_by_spammer_worker.rb
- app/controllers/admin/subforem_moderators/moderators_controller.rb
- app/services/subforem_moderators/add.rb
- app/services/subforem_moderators/add_trusted_role.rb
- spec/services/subforem_moderators/remove_spec.rb

## Functional Overview

This specification defines the expected behavior of `SubforemModerators::Remove` within the moderation domain.

### Behavioral Areas

- **call**: Ensures correct behavior under the specified conditions
- **when user has community mod newsletter enabled**: removes the subforem moderator role from the user
- **when user does not have community mod newsletter enabled**: removes the subforem moderator role from the user

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/notifications/remove_by_spammer.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/subforem_moderators/remove.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/tag_moderators/remove.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/notifications/remove_by_spammer_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/subforem_moderators/moderators_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/subforem_moderators/add.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/subforem_moderators/add_trusted_role.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: removes the subforem moderator role from the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes the subforem moderator role from the user

### S-2: updates the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the user

### S-3: clears the cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** clears the cache

### S-4: manages mailchimp list

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** manages mailchimp list

### S-5: removes the subforem moderator role from the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes the subforem moderator role from the user

### S-6: does not update notification settings

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not update notification settings

