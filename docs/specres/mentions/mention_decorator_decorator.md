---
id: "01KHY7Q1H9N7ESBG3125JH6JC7"
name: "mention_decorator_decorator"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/decorators/mention_decorator.rb
- spec/decorators/mention_decorator_spec.rb

## Functional Overview

This specification defines the expected behavior of `MentionDecorator` within the mentions domain.

### Behavioral Areas

- **formatted_mentionable_type**: Ensures correct behavior under the specified conditions
- **mentioned_by_blocked_user?**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Decorator**: `app/decorators/mention_decorator.rb` -- presentation logic and view-model enrichment


## Scenarios

### S-1: returns the correct mentionable type for mentions on articles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct mentionable type for mentions on articles

### S-2: returns the correct mentionable type for mentions on comments

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct mentionable type for mentions on comments

### S-3: returns true if mentioned user has blocked the mentioner

- **Given** mentioned user has blocked the mentioner
- **When** the action is triggered
- **Then** returns true

### S-4: returns false if mentioned user has not blocked the mentioner

- **Given** mentioned user has not blocked the mentioner
- **When** the action is triggered
- **Then** returns false

