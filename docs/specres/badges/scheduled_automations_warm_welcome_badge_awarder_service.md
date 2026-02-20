---
id: "01KHY7Q0B8HKA8XMS6KYXS87QZ"
name: "scheduled_automations_warm_welcome_badge_awarder_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/scheduled_automations/warm_welcome_badge_awarder.rb
- app/services/scheduled_automations/article_content_badge_awarder.rb
- app/services/scheduled_automations/first_post_badge_awarder.rb
- spec/services/scheduled_automations/warm_welcome_badge_awarder_spec.rb

## Functional Overview

This specification defines the expected behavior of `ScheduledAutomations::WarmWelcomeBadgeAwarder` within the badges domain.

### Behavioral Areas

- **.call**: Ensures correct behavior under the specified conditions
- **call**: Ensures correct behavior under the specified conditions
- **when badge does not exist**: awards badges to users with helpful comments
- **when welcome thread does not exist**: does not award badges for spam comments
- **when welcome thread exists**: Ensures correct behavior under the specified conditions
- **with helpful comments**: returns success with zero users awarded
- **with spam comments**: returns success with zero users awarded
- **with low quality comments**: returns success with zero users awarded

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/scheduled_automations/warm_welcome_badge_awarder.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/scheduled_automations/article_content_badge_awarder.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/scheduled_automations/first_post_badge_awarder.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns a result object

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a result object

### S-2: returns a failure result

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a failure result

### S-3: returns success with zero users awarded

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns success with zero users awarded

### S-4: awards badges to users with helpful comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** awards badges to users with helpful comments

### S-5: includes proper message in badge achievement

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes proper message in badge achievement

### S-6: does not award badges for spam comments

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award badges for spam comments

### S-7: does not award badges for low quality comments

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award badges for low quality comments

### S-8: does not award badges for unhelpful comments

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award badges for unhelpful comments

### S-9: does not award badges for comments outside the lookback window

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award badges for comments outside the lookback window

### S-10: does not award badges for comments before last_run_at

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award badges for comments before last_run_at

### S-11: does not award badges to users who received it within the last 6.5 days

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award badges to users who received it within the last 6.5 days

### S-12: allows awarding badge again after 6.5 days

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows awarding badge again after 6.5 days

