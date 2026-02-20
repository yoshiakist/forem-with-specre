---
id: "01KHY7Q0ARYP2494A2KX21AKKJ"
name: "badges_award_streak_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/badges/award_streak.rb
- app/controllers/admin/badges_controller.rb
- app/controllers/api/v0/badges_controller.rb
- app/controllers/api/v1/badges_controller.rb
- app/controllers/badges_controller.rb
- app/controllers/concerns/api/badges_controller.rb
- app/services/badges/award.rb
- app/services/badges/award_beloved_comment.rb
- app/services/badges/award_community_wellness.rb
- app/services/badges/award_contributor.rb
- app/services/badges/award_contributor_from_github.rb
- spec/services/badges/award_streak_spec.rb

## Functional Overview

This specification defines the expected behavior of `Badges::AwardStreak` within the badges domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/badges/award_streak.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/admin/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/badges_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/badges/award.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/badges/award_beloved_comment.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/badges/award_community_wellness.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/badges/award_contributor.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/badges/award_contributor_from_github.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: awards badge to users with four straight weeks of articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** awards badge to users with four straight weeks of articles

### S-2: does not award the badge to not qualified users

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award the badge to not qualified users

