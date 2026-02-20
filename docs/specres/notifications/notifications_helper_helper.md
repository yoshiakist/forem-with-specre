---
id: "01KHY7Q057M48GYCB9MDEYK3XK"
name: "notifications_helper_helper"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/helpers/notifications_helper.rb
- spec/helpers/notifications_helper_spec.rb

## Functional Overview

This specification defines the expected behavior of `NotificationsHelper` within the notifications domain.

### Behavioral Areas

- **with a moderation notification**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **View helper**: `app/helpers/notifications_helper.rb` -- shared view utility methods


## Scenarios

### S-1: returns a new category image from ReactionCategory

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a new category image from ReactionCategory

### S-2: returns a heart for unrecognized category

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a heart for unrecognized category

### S-3: returns the commenting user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the commenting user

### S-4: extracts the commenting user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** extracts the commenting user

