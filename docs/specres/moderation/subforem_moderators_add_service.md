---
id: "01KHY7Q0NFTF0PZVMWQB8QE78F"
name: "subforem_moderators_add_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/subforem_moderators/add.rb
- app/services/subforem_moderators/add_trusted_role.rb
- app/services/tag_moderators/add.rb
- app/services/tag_moderators/add_trusted_role.rb
- app/controllers/admin/subforem_moderators/moderators_controller.rb
- app/services/subforem_moderators/remove.rb
- spec/services/subforem_moderators/add_spec.rb

## Functional Overview

This specification defines the expected behavior of `SubforemModerators::Add` within the moderation domain.

### Behavioral Areas

- **call**: calls AddTrustedRole
- **when successful**: Ensures correct behavior under the specified conditions
- **when notification setting update fails**: updates the user

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/subforem_moderators/add.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/subforem_moderators/add_trusted_role.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/tag_moderators/add.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/tag_moderators/add_trusted_role.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/admin/subforem_moderators/moderators_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/subforem_moderators/remove.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: adds the subforem moderator role to the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds the subforem moderator role to the user

### S-2: updates the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the user

### S-3: calls AddTrustedRole

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls AddTrustedRole

### S-4: sends confirmation email

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends confirmation email

### S-5: clears the cache

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** clears the cache

### S-6: returns success result

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns success result

### S-7: returns failure result with errors

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns failure result with errors

### S-8: does not add the role

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not add the role

