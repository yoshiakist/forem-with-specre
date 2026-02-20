---
id: "01KHY7Q0B2XBT57NP69NJCNYXX"
name: "badges_award_yearly_club_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/badges/award_yearly_club.rb
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
- spec/services/badges/award_yearly_club_spec.rb

## Functional Overview

This specification defines the expected behavior of `Badges::AwardYearlyClub` within the badges domain.

### Behavioral Areas

- **.call**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/badges/award_yearly_club.rb` -- business logic orchestration and domain operations
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

### S-1: awards birthday badge to birthday folks who registered a year ago

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** awards birthday badge to birthday folks who registered a year ago

### S-2: rewards 2-year birthday badge to birthday folks who registered 2 years ago

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rewards 2-year birthday badge to birthday folks who registered 2 years ago

### S-3: rewards 3-year birthday badge to birthday folks who registered 3 years ago

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rewards 3-year birthday badge to birthday folks who registered 3 years ago

