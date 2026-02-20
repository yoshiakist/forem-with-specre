---
id: "01KHY7Q09M2408X7CC5STQ3SBA"
name: "badge_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/badge_achievements_controller.rb
- app/controllers/admin/badge_automations_controller.rb
- app/controllers/admin/badges_controller.rb
- app/controllers/api/v0/badge_achievements_controller.rb
- app/controllers/api/v0/badges_controller.rb
- app/controllers/api/v1/badge_achievements_controller.rb
- app/controllers/api/v1/badges_controller.rb
- app/controllers/badges_controller.rb
- app/controllers/concerns/api/badge_achievements_controller.rb
- app/controllers/concerns/api/badges_controller.rb
- app/models/badge.rb
- app/models/badge_achievement.rb
- app/policies/badge_achievement_policy.rb
- app/policies/badge_policy.rb
- app/services/ai/badge_criteria_assessor.rb
- spec/models/badge_spec.rb

## Functional Overview

This specification defines the expected behavior of `Badge` within the badges domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions
- **class methods**: Ensures correct behavior under the specified conditions
- **.id_for_slug**: Ensures correct behavior under the specified conditions
- **slug**: returns the id of an existing slug

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/badge_achievements_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/badge_automations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/badge_achievements_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/badge_achievements_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/badge_achievements_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/badges_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/badge.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/badge_achievement.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- have many badge achievements.dependent restrict with error
- have many tags.dependent restrict with error
- have many users.through badge achievements
- validate presence of badge image
- validate presence of description
- validate presence of title
- validate uniqueness of title

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: returns the id of an existing slug

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the id of an existing slug

### S-3: returns nil for non-existing slugs

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns nil for non-existing slugs

### S-4: generates the correct slug for C

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** generates the correct slug for C

### S-5: generates the correct slug for C#

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** generates the correct slug for C#

### S-6: generates the correct slug for 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** generates the correct slug for 

