---
id: "01KHY7PZT2RQAJ88J4N3AKPZJD"
name: "user_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/user_tag.rb
- app/liquid_tags/user_subscription_tag.rb
- app/models/liquid_tags/user_subscription_tag.rb
- app/services/users/approved_liquid_tags.rb
- spec/liquid_tags/user_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `UserTag` within the users domain.

### Behavioral Areas

- **when given valid id_code**: Ensures correct behavior under the specified conditions
- **when given an invalid username**: renders a missing username and name

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/user_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/user_subscription_tag.rb` -- custom Markdown/Liquid embed rendering
- **Model layer**: `app/models/liquid_tags/user_subscription_tag.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/users/approved_liquid_tags.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: renders the proper user name

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper user name

### S-2: renders image html

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders image html

### S-3: renders the proper follow button for a user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper follow button for a user

### S-4: renders a missing username and name

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders a missing username and name

