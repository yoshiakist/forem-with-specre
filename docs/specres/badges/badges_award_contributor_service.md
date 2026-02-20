---
id: "01KHY7Q0A6V8M2EJNNA4NAC2BT"
name: "badges_award_contributor_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/badges/award_contributor.rb
- app/services/badges/award_contributor_from_github.rb
- app/controllers/admin/badges_controller.rb
- app/controllers/api/v0/badges_controller.rb
- app/controllers/api/v1/badges_controller.rb
- app/controllers/badges_controller.rb
- app/controllers/concerns/api/badges_controller.rb
- app/services/badges/award.rb
- app/services/badges/award_beloved_comment.rb
- app/services/badges/award_community_wellness.rb
- app/services/badges/award_eight_week_streak.rb
- app/services/badges/award_fab_five.rb
- spec/services/badges/award_contributor_spec.rb

## Functional Overview

This specification defines the expected behavior of `Badges::AwardContributor` within the badges domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/badges/award_contributor.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/badges/award_contributor_from_github.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/admin/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/badges_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/badges/award.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/badges/award_beloved_comment.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/badges/award_community_wellness.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/badges/award_eight_week_streak.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/badges/award_fab_five.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: awards contributor badge to users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** awards contributor badge to users

