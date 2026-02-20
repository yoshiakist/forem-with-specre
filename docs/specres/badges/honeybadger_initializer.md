---
id: "01KHY7Q09C00J4EYGWNZGJ0GGH"
name: "honeybadger_initializer"
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
- spec/initializers/honeybadger_spec.rb

## Functional Overview

This specification defines the expected behavior of `Honeybadger` within the badges domain.

### Behavioral Areas

- **when configuration is loaded**: Ensures correct behavior under the specified conditions
- **when error is raised from an internal route**: sets fingerprint to internal

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/badge_achievements_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/badge_automations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/badge_achievements_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/badge_achievements_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: ignores requested exceptions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** ignores requested exceptions

### S-2: sets fingerprint to internal

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets fingerprint to internal

