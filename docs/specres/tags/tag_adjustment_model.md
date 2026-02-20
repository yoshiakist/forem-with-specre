---
id: "01KHY7Q0BGKJ6PX3G2AHDW5D6P"
name: "tag_adjustment_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/tag_adjustments_controller.rb
- app/models/tag_adjustment.rb
- app/services/tag_adjustment_creation_service.rb
- app/services/tag_adjustment_update_service.rb
- app/workers/notifications/tag_adjustment_notification_worker.rb
- app/models/tag_subforem_relationship.rb
- spec/models/tag_adjustment_spec.rb

## Functional Overview

This specification defines the expected behavior of `TagAdjustment` within the tags domain.

### Behavioral Areas

- **privileges**: Ensures correct behavior under the specified conditions
- **allowed attribute states**: Ensures correct behavior under the specified conditions
- **validates article tag_list**: does not allow addition on articles with 4 tags

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/tag_adjustments_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/tag_adjustment.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/tag_adjustment_creation_service.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/tag_adjustment_update_service.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/notifications/tag_adjustment_notification_worker.rb` -- asynchronous job processing
- **Model layer**: `app/models/tag_subforem_relationship.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- validate presence of tag name
- validate presence of adjustment type
- validate presence of status
- have many notifications.dependent delete all

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: allows tag mods to create for their tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows tag mods to create for their tags

### S-3: allows tag mods to create a tag adjustment for a tag that has been adjusted by a...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows tag mods to create a tag adjustment for a tag that has been adjusted by another tag mod

### S-4: does not allow tag mods to create a tag adjustment for other tags

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow tag mods to create a tag adjustment for other tags

### S-5: allows admins to create a tag adjustment for any tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows admins to create a tag adjustment for any tags

### S-6: allows admins and super moderators to create a tag adjustment for a tag that was...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows admins and super moderators to create a tag adjustment for a tag that was adjusted by another admin

### S-7: does not allow normal users to create a tag adjustment for any tags

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow normal users to create a tag adjustment for any tags

### S-8: allows addition adjustment_types

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows addition adjustment_types

### S-9: allows removal adjustment_types

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows removal adjustment_types

### S-10: disallows improper adjustment_types

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** disallows improper adjustment_types

### S-11: allows proper status

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows proper status

### S-12: disallows improper status

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** disallows improper status

### S-13: does not allow addition on articles with 4 tags

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow addition on articles with 4 tags

