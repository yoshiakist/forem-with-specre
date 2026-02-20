---
id: "01KHY7Q0NMRA3FC70SQ7CRZVNE"
name: "tag_moderators_add_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/subforem_moderators/add.rb
- app/services/subforem_moderators/add_trusted_role.rb
- app/services/tag_moderators/add.rb
- app/services/tag_moderators/add_trusted_role.rb
- app/services/tag_moderators/remove.rb
- spec/services/tag_moderators/add_spec.rb

## Functional Overview

This specification defines the expected behavior of `TagModerators::Add` within the moderation domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/subforem_moderators/add.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/subforem_moderators/add_trusted_role.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/tag_moderators/add.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/tag_moderators/add_trusted_role.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/tag_moderators/remove.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: adds tag moderator role

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds tag moderator role

### S-2: updates user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates user

### S-3: calls Moderators::AddTrustedRole

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls Moderators::AddTrustedRole

### S-4: autosupports tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** autosupports tag

### S-5: returns success when needed

- **Given** the system is in a standard operational state
- **When** needed
- **Then** returns success

### S-6: returns error when notification setting is not updated

- **Given** the system is in a standard operational state
- **When** notification setting is not updated
- **Then** returns error

