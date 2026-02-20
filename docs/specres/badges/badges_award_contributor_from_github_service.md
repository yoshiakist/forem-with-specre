---
id: "01KHY7Q0A3RX6W57H3ZZ3MD6F8"
name: "badges_award_contributor_from_github_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/badges/award_contributor_from_github.rb
- app/controllers/admin/badges_controller.rb
- app/controllers/api/v0/badges_controller.rb
- app/controllers/api/v1/badges_controller.rb
- app/controllers/badges_controller.rb
- app/controllers/concerns/api/badges_controller.rb
- app/services/badges/award.rb
- app/services/badges/award_beloved_comment.rb
- app/services/badges/award_community_wellness.rb
- app/services/badges/award_contributor.rb
- app/services/badges/award_eight_week_streak.rb
- spec/services/badges/award_contributor_from_github_spec.rb

## Functional Overview

This specification defines the expected behavior of `Badges::AwardContributorFromGithub` within the badges domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/badges/award_contributor_from_github.rb` -- business logic orchestration and domain operations
- **Controller layer**: `app/controllers/admin/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/badges_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/badges_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/badges/award.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/badges/award_beloved_comment.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/badges/award_community_wellness.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/badges/award_contributor.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/badges/award_eight_week_streak.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: won

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** won

### S-2: awards contributor badge

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** awards contributor badge

### S-3: awards contributor badge once

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** awards contributor badge once

### S-4: awards bronze contributor badge

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** awards bronze contributor badge

### S-5: awards silver contributor badge

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** awards silver contributor badge

### S-6: awards gold contributor badge

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** awards gold contributor badge

### S-7: awards single commit contributors

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** awards single commit contributors

