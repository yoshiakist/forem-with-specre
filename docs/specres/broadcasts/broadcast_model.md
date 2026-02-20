---
id: "01KHY7Q1DDE8S25J768HW18Z78"
name: "broadcast_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/broadcasts_controller.rb
- app/helpers/broadcasts_helper.rb
- app/models/broadcast.rb
- spec/models/broadcast_spec.rb

## Functional Overview

This specification defines the expected behavior of `Broadcast` within the broadcasts domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/broadcasts_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/broadcasts_helper.rb` -- shared view utility methods
- **Model layer**: `app/models/broadcast.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- validate presence of title
- validate presence of type of
- validate presence of processed html
- validate inclusion of type of.in array %w[Announcement Welcome]
- validate inclusion of banner style.in array %w[default brand success warning error]
- validate uniqueness of title.scoped to type of
- have many notifications.dependent destroy

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: validates that only one Broadcast with a type_of Announcement can be active

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates that only one Broadcast with a type_of Announcement can be active

### S-3: updates the Broadcast

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the Broadcast

