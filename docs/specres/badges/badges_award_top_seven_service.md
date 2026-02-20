---
id: "01KHY7Q0B06HS0HN1QY8BE535B"
name: "badges_award_top_seven_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/badges/award_top_seven.rb
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
- spec/services/badges/award_top_seven_spec.rb

## Functional Overview

This specification defines the expected behavior of `Badges::AwardTopSeven` within the badges domain.

### Behavioral Areas

- **.call**: Ensures correct behavior under the specified conditions
- **when awarding badges**: Ensures correct behavior under the specified conditions
- **when applying reputation modifier changes**: logs the reputation modifier changes
- **when no positive reactions exist**: multiplies positive reactors
- **when user has no articles**: awards top seven badge to users
- **when reputation modifier is already at maximum**: logs the reputation modifier changes
- **when using custom message markdown**: uses the custom message
- **.default_message_markdown**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/badges/award_top_seven.rb` -- business logic orchestration and domain operations
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

### S-1: awards top seven badge to users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** awards top seven badge to users

### S-2: creates badge achievements for the correct users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates badge achievements for the correct users

### S-3: doubles the badge recipient

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doubles the badge recipient

### S-4: caps the badge recipient

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** caps the badge recipient

### S-5: multiplies positive reactors

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** multiplies positive reactors

### S-6: caps positive reactors

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** caps positive reactors

### S-7: does not affect users who gave negative reactions

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not affect users who gave negative reactions

### S-8: only considers reactions from the last week

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** only considers reactions from the last week

### S-9: handles multiple badge recipients independently

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles multiple badge recipients independently

### S-10: logs the reputation modifier changes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs the reputation modifier changes

### S-11: still doubles the badge recipient

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** still doubles the badge recipient

### S-12: logs zero positive reactors

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** logs zero positive reactors

