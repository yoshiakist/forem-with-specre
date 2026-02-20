---
id: "01KHY7Q0AE51Z0TSSTAWJFWXNJ"
name: "badges_award_first_post_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/badges/award_first_post.rb
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
- spec/services/badges/award_first_post_spec.rb

## Functional Overview

This specification defines the expected behavior of `Badges::AwardFirstPost` within the badges domain.

### Behavioral Areas

- **.call**: Ensures correct behavior under the specified conditions
- **when the article is created outside the award window**: does not award the badge for an article created more than a week ago
- **when the article is created within the award window**: does not award the badge for an article created more than a week ago
- **when the user has a spam or suspended role**: does not award the badge to a spam user

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/badges/award_first_post.rb` -- business logic orchestration and domain operations
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

### S-1: does not award the badge for an article created more than a week ago

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award the badge for an article created more than a week ago

### S-2: does not award the badge for an article created less than an hour ago

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award the badge for an article created less than an hour ago

### S-3: awards the badge

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** awards the badge

### S-4: does not award the badge if the article score is less than zero

- **Given** the article score is less than zero
- **When** the action is triggered
- **Then** does not award the badge

### S-5: does not award the badge to a spam user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award the badge to a spam user

### S-6: does not award the badge to a suspended user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award the badge to a suspended user

