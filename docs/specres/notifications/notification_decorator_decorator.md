---
id: "01KHY7Q054BC0Z4JZQJSDC051D"
name: "notification_decorator_decorator"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/decorators/notification_decorator.rb
- spec/decorators/notification_decorator_spec.rb

## Functional Overview

This specification defines the expected behavior of `NotificationDecorator` within the notifications domain.

### Behavioral Areas

- **with serialization**: Ensures correct behavior under the specified conditions
- **mocked_object**: Ensures correct behavior under the specified conditions
- **milestone_type**: Ensures correct behavior under the specified conditions
- **milestone_count**: Ensures correct behavior under the specified conditions
- **reaction to a article**: responds to reaction_category
- **reaction to a comment**: responds to reaction_category
- **notification relating to an article**: returns empty struct if the notification is new
- **when a user may have a subscription**: responds to user fields (even if blank)

### Implementation Architecture

The behavior is implemented across the following layers:

- **Decorator**: `app/decorators/notification_decorator.rb` -- presentation logic and view-model enrichment


## Scenarios

### S-1: serializes both the decorated object IDs and decorated methods

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** serializes both the decorated object IDs and decorated methods

### S-2: serializes collections of decorated objects

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** serializes collections of decorated objects

### S-3: returns empty struct if the notification is new

- **Given** the notification is new
- **When** the action is triggered
- **Then** returns empty struct

### S-4: returns empty struct class and its name if the notification is new

- **Given** the notification is new
- **When** the action is triggered
- **Then** returns empty struct class and its name

### S-5: returns class name and id for the reactable in a struct

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns class name and id for the reactable in a struct

### S-6: returns struct class and its name

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns struct class and its name

### S-7: returns empty string if there is no action

- **Given** there is no action
- **When** the action is triggered
- **Then** returns empty string

### S-8: returns the type of the milestone action

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the type of the milestone action

### S-9: is a milestone type

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is a milestone type

### S-10: is also a milestone type if has milestone type

- **Given** has milestone type
- **When** the action is triggered
- **Then** is also a milestone type

### S-11: returns empty string if there is no action

- **Given** there is no action
- **When** the action is triggered
- **Then** returns empty string

### S-12: returns the count of the milestone action

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the count of the milestone action

