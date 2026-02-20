---
id: "01KHY7Q0ATM8G9BX8AQK3WJ0D9"
name: "badges_award_tag_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/badges/award_tag.rb
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
- spec/services/badges/award_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `Badges::AwardTag` within the badges domain.

### Behavioral Areas

- **when award_tag_minimum_score setting is different than default**: Ensures correct behavior under the specified conditions
- **when award_tag_minimum_score is 100 and the article score is greater than it**: awards badge if qualifying article by score and tagged appropriately

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/badges/award_tag.rb` -- business logic orchestration and domain operations
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

### S-1: awards badge if qualifying article by score and tagged appropriately

- **Given** qualifying article by score and tagged appropriately
- **When** the action is triggered
- **Then** awards badge

### S-2: renders html for message

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders html for message

### S-3: does not award badge if qualifying article by score but not tagged appropriately

- **Given** qualifying article by score but not tagged appropriately
- **When** the action is triggered
- **Then** does not award badge

### S-4: does not award badge if qualifying article by score but not from past week

- **Given** qualifying article by score but not from past week
- **When** the action is triggered
- **Then** does not award badge

### S-5: does not award badge if tagged appropriately but not published

- **Given** tagged appropriately but not published
- **When** the action is triggered
- **Then** does not award badge

### S-6: does not award badge to user who has previously won

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award badge to user who has previously won

### S-7: awards badge if qualifying article by score and tagged appropriately

- **Given** qualifying article by score and tagged appropriately
- **When** the action is triggered
- **Then** awards badge

### S-8: awards badge if qualifying article by score and tagged appropriately

- **Given** qualifying article by score and tagged appropriately
- **When** the action is triggered
- **Then** awards badge

