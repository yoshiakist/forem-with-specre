---
id: "01KHY7Q02M69K1D5GQRSAKNBT2"
name: "tags_user_updates_a_tag_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/user_subscription_tag.rb
- app/liquid_tags/user_tag.rb
- app/models/liquid_tags/user_subscription_tag.rb
- app/services/users/approved_liquid_tags.rb
- spec/system/tags/user_updates_a_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `"User` within the users domain.

### Behavioral Areas

- **User updates a tag**: Ensures correct behavior under the specified conditions
- **Update tag as a super_admin**: defaults to black and white upon update
- **when no colors have been chosen for the tag**: Ensures correct behavior under the specified conditions
- **when colors have already been chosen for the tag**: Ensures correct behavior under the specified conditions
- **Update tag as a tag_moderator**: defaults to black and white upon update
- **when no colors have been chosen for the tag**: Ensures correct behavior under the specified conditions
- **when colors have already been chosen for the tag**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/user_subscription_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/user_tag.rb` -- custom Markdown/Liquid embed rendering
- **Model layer**: `app/models/liquid_tags/user_subscription_tag.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/users/approved_liquid_tags.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: defaults to black and white upon update

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** defaults to black and white upon update

### S-2: remains the same color it was unless otherwise updated via the color picker

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** remains the same color it was unless otherwise updated via the color picker

### S-3: defaults to black and white upon update

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** defaults to black and white upon update

### S-4: remains the same color it was unless otherwise updated via the color picker

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** remains the same color it was unless otherwise updated via the color picker

