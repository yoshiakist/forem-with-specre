---
id: "01KHY7Q09EJ4VFGDDTN9ECZEG0"
name: "badge_achievement_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/badge_achievements_controller.rb
- app/controllers/api/v0/badge_achievements_controller.rb
- app/controllers/api/v1/badge_achievements_controller.rb
- app/controllers/concerns/api/badge_achievements_controller.rb
- app/models/badge_achievement.rb
- app/policies/badge_achievement_policy.rb
- app/workers/notifications/new_badge_achievement_worker.rb
- app/models/badge.rb
- spec/models/badge_achievement_spec.rb

## Functional Overview

This specification defines the expected behavior of `BadgeAchievement` within the badges domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions
- **Top 7 badge reputation modifier callback**: doubles the badge recipient
- **when creating a Top 7 badge achievement**: doubles the badge recipient
- **when creating a non-Top 7 badge achievement**: doubles the badge recipient
- **when user has no articles**: does not affect users who gave negative reactions
- **when reputation modifier is already at maximum**: logs the reputation modifier changes
- **when no positive reactions exist**: awards credits after create if credits_awarded exist

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/badge_achievements_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/badge_achievements_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/badge_achievements_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/badge_achievements_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/badge_achievement.rb` -- data persistence, validations, and associations
- **Policy layer**: `app/policies/badge_achievement_policy.rb` -- authorization and access control rules
- **Background worker**: `app/workers/notifications/new_badge_achievement_worker.rb` -- asynchronous job processing
- **Model layer**: `app/models/badge.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to user
- belong to badge
- belong to rewarder.class name "User".optional
- validate uniqueness of badge id.scoped to user id

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: turns rewarding_context_message_markdown into rewarding_context_message HTML

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** turns rewarding_context_message_markdown into rewarding_context_message HTML

### S-3: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-4: awards credits after create if credits_awarded exist

- **Given** credits_awarded exist
- **When** the action is triggered
- **Then** awards credits after create

### S-5: notifies recipients after commit

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** notifies recipients after commit

### S-6: doubles the badge recipient

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doubles the badge recipient

### S-7: caps the badge recipient

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** caps the badge recipient

### S-8: multiplies positive reactors

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** multiplies positive reactors

### S-9: caps positive reactors

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** caps positive reactors

### S-10: does not affect users who gave negative reactions

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not affect users who gave negative reactions

### S-11: only considers reactions from the last week

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** only considers reactions from the last week

### S-12: logs the reputation modifier changes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs the reputation modifier changes

### S-13: does not change reputation modifiers

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not change reputation modifiers

