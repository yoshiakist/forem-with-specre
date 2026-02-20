---
id: "01KHY7Q0GFFKFR26G6TPNGGNPN"
name: "reaction_handler_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/reaction_handler.rb
- app/services/calculate_reaction_points.rb
- app/services/notifications/reactions/reaction_data.rb
- app/services/notifications/reactions/send.rb
- app/services/slack/messengers/reaction_vomit.rb
- app/services/spam/reaction_ring_detector.rb
- app/services/users/confirm_flag_reactions.rb
- spec/services/reaction_handler_spec.rb

## Functional Overview

This specification defines the expected behavior of `ReactionHandler` within the reactions domain.

### Behavioral Areas

- **create**: justs create
- **when no existing/matching reaction by user**: ignores other existing reactions
- **when the article is written for an organization**: records a feed event for articles reached through a feed
- **when the reaction is not a public reaction or bookmark**: ignores other existing reactions
- **when there**: sends the notifications immediately if there was an existing reaction
- **when the reaction is a bookmark**: ignores other existing reactions
- **when there**: sends the notifications immediately if there was an existing reaction
- **when the reactable is a comment**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/reaction_handler.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/calculate_reaction_points.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/reactions/reaction_data.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/reactions/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/slack/messengers/reaction_vomit.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/spam/reaction_ring_detector.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/confirm_flag_reactions.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: justs create

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** justs create

### S-2: ignores other existing reactions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** ignores other existing reactions

### S-3: sends a notification to the author

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends a notification to the author

### S-4: records a feed event for articles reached through a feed

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** records a feed event for articles reached through a feed

### S-5: does not record a feed event for articles that were not reached through a feed

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not record a feed event for articles that were not reached through a feed

### S-6: sends a notification to both the author and the organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends a notification to both the author and the organization

### S-7: does not record a feed event

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not record a feed event

### S-8: does nothing

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** does nothing

### S-9: ignores other existing reactions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** ignores other existing reactions

### S-10: does not send a notification to the author

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not send a notification to the author

### S-11: does not send a notification to the author

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not send a notification to the author

### S-12: records a feed event if reached through a feed

- **Given** reached through a feed
- **When** the action is triggered
- **Then** records a feed event

