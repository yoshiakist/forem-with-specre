---
id: "01KHY7Q0GCG2H20EZE8EJ12QTW"
name: "calculate_reaction_points_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/calculate_reaction_points.rb
- app/services/notifications/reactions/reaction_data.rb
- app/services/notifications/reactions/send.rb
- app/services/reaction_handler.rb
- app/services/slack/messengers/reaction_vomit.rb
- app/services/spam/reaction_ring_detector.rb
- app/services/users/confirm_flag_reactions.rb
- spec/services/calculate_reaction_points_spec.rb

## Functional Overview

This specification defines the expected behavior of `CalculateReactionPoints` within the reactions domain.

### Behavioral Areas

- **when reaction is to comment on author**: assigns 0 points if reaction is invalid
- **when newish user**: assigns fractional points to new users on create

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/calculate_reaction_points.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/reactions/reaction_data.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/reactions/send.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/reaction_handler.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/slack/messengers/reaction_vomit.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/spam/reaction_ring_detector.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/confirm_flag_reactions.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: assigns 0 points if reaction is invalid

- **Given** reaction is invalid
- **When** the action is triggered
- **Then** assigns 0 points

### S-2: assigns extra 5 points

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** assigns extra 5 points

### S-3: does not extra 5 points if comment from other author

- **Given** comment from other author
- **When** the action is triggered
- **Then** does not extra 5 points

### S-4: assigns the correct points if reaction is confirmed

- **Given** reaction is confirmed
- **When** the action is triggered
- **Then** assigns the correct points

### S-5: assigns fractional points to new users on create

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** assigns fractional points to new users on create

### S-6: assigns full points to new user who is also trusted

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** assigns full points to new user who is also trusted

### S-7: assigns full points to new users who is admin

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** assigns full points to new users who is admin

### S-8: Does not assign new fractional logic on re-save

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system Does not assign new fractional logic on re-save

