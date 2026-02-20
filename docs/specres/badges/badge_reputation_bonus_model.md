---
id: "01KHY7Q09H5J4HGY1X1K4S65BB"
name: "badge_reputation_bonus_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/badge.rb
- app/models/badge_achievement.rb
- spec/models/badge_reputation_bonus_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Article` within the badges domain.

### Behavioral Areas

- **Article Badge Reputation Bonus**: calculates the reputation bonus as the square root of the sum of badge weights

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/badge.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/badge_achievement.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: calculates the reputation bonus as the square root of the sum of badge weights

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calculates the reputation bonus as the square root of the sum of badge weights

### S-2: handles zero bonus weight correctly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles zero bonus weight correctly

