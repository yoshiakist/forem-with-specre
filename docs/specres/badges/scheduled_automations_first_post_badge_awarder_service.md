---
id: "01KHY7Q0B57XY6RQ8KYV4ZTK0B"
name: "scheduled_automations_first_post_badge_awarder_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/scheduled_automations/first_post_badge_awarder.rb
- app/services/scheduled_automations/article_content_badge_awarder.rb
- app/services/scheduled_automations/warm_welcome_badge_awarder.rb
- spec/services/scheduled_automations/first_post_badge_awarder_spec.rb

## Functional Overview

This specification defines the expected behavior of `ScheduledAutomations::FirstPostBadgeAwarder` within the badges domain.

### Behavioral Areas

- **.call**: Ensures correct behavior under the specified conditions
- **call**: Ensures correct behavior under the specified conditions
- **when configuration is invalid**: Ensures correct behavior under the specified conditions
- **when organization_id is missing**: Ensures correct behavior under the specified conditions
- **when badge_slug is missing**: Ensures correct behavior under the specified conditions
- **when organization does not exist**: awards badges to users who posted their first post under the organization
- **when badge does not exist**: awards badges to users who posted their first post under the organization
- **when configuration is valid**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/scheduled_automations/first_post_badge_awarder.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/scheduled_automations/article_content_badge_awarder.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/scheduled_automations/warm_welcome_badge_awarder.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns a result object

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a result object

### S-2: returns a failure result

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a failure result

### S-3: returns a failure result

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a failure result

### S-4: returns a failure result

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a failure result

### S-5: returns a failure result

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a failure result

### S-6: awards badges to users who posted their first post under the organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** awards badges to users who posted their first post under the organization

### S-7: does not award badges to users who already have the badge

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award badges to users who already have the badge

### S-8: does not award badges for unpublished articles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award badges for unpublished articles

### S-9: does not award badges for articles under different organizations

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award badges for articles under different organizations

### S-10: does not award badges to banished users

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award badges to banished users

### S-11: includes proper message in badge achievement

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes proper message in badge achievement

### S-12: only awards badges for posts published since last_run_at (minus 15 minutes)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** only awards badges for posts published since last_run_at (minus 15 minutes)

