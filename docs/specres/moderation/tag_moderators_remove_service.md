---
id: "01KHY7Q0NSS391MYG02ERT60NZ"
name: "tag_moderators_remove_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/notifications/remove_by_spammer.rb
- app/services/subforem_moderators/remove.rb
- app/services/tag_moderators/remove.rb
- app/workers/notifications/remove_by_spammer_worker.rb
- app/services/tag_moderators/add.rb
- app/services/tag_moderators/add_trusted_role.rb
- spec/services/tag_moderators/remove_spec.rb

## Functional Overview

This specification defines the expected behavior of `TagModerators::Remove` within the moderation domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/notifications/remove_by_spammer.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/subforem_moderators/remove.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/tag_moderators/remove.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/notifications/remove_by_spammer_worker.rb` -- asynchronous job processing
- **Service layer**: `app/services/tag_moderators/add.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/tag_moderators/add_trusted_role.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: removes the tag_moderator role from the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes the tag_moderator role from the user

