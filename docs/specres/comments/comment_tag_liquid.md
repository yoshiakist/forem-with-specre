---
id: "01KHY7PZP3PX4PW73AQY8J1XP3"
name: "comment_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/comment_tag.rb
- spec/liquid_tags/comment_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `CommentTag` within the comments domain.

### Behavioral Areas

- **when given valid id_code**: Ensures correct behavior under the specified conditions
- **when rendered**: Ensures correct behavior under the specified conditions
- **with the legacy**: Ensures correct behavior under the specified conditions
- **when given invalid id_code**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/comment_tag.rb` -- custom Markdown/Liquid embed rendering


## Scenarios

### S-1: fetches the target comment and render properly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** fetches the target comment and render properly

### S-2: renders 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders 

### S-3: shows the comment date

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the comment date

### S-4: embeds the comment published timestamp

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** embeds the comment published timestamp

### S-5: renders properly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders properly

### S-6: raises an error

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises an error

