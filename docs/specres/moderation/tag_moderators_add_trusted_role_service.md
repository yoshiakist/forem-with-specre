---
id: "01KHY7Q0NQFQDMJHCB2WT4QWFZ"
name: "tag_moderators_add_trusted_role_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/subforem_moderators/add_trusted_role.rb
- app/services/tag_moderators/add_trusted_role.rb
- app/services/tag_moderators/add.rb
- app/services/tag_moderators/remove.rb
- spec/services/tag_moderators/add_trusted_role_spec.rb

## Functional Overview

This specification defines the expected behavior of `TagModerators::AddTrustedRole` within the moderation domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/subforem_moderators/add_trusted_role.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/tag_moderators/add_trusted_role.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/tag_moderators/add.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/tag_moderators/remove.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: adds the trusted role to a user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds the trusted role to a user

### S-2: does not add the fole for suspended users

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not add the fole for suspended users

### S-3: signs the user up for the community mods newsletter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** signs the user up for the community mods newsletter

