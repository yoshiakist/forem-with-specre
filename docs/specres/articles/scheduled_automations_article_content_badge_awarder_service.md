---
id: "01KHY7PZJY4BBA8TMJ9VACRRM8"
name: "scheduled_automations_article_content_badge_awarder_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/scheduled_automations/article_content_badge_awarder.rb
- spec/services/scheduled_automations/article_content_badge_awarder_spec.rb

## Functional Overview

This specification defines the expected behavior of `ScheduledAutomations::ArticleContentBadgeAwarder` within the articles domain.

### Behavioral Areas

- **.call**: Ensures correct behavior under the specified conditions
- **call**: Ensures correct behavior under the specified conditions
- **when badge does not exist**: awards badges to users with qualifying articles
- **when badge_slug is missing**: processes all articles when no keywords provided
- **when criteria is missing**: processes all articles when no keywords provided
- **when articles exist**: awards badges to users with qualifying articles
- **with qualifying articles matching keywords**: awards badges to users with qualifying articles
- **with articles that don**: awards badges to users with qualifying articles

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/scheduled_automations/article_content_badge_awarder.rb` -- business logic orchestration and domain operations


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

### S-5: awards badges to users with qualifying articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** awards badges to users with qualifying articles

### S-6: includes proper message in badge achievement

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes proper message in badge achievement

### S-7: does not award badges for articles that don

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award badges for articles that don

### S-8: does not award badges for articles below minimum threshold

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award badges for articles below minimum threshold

### S-9: does not award badges for articles that don

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award badges for articles that don

### S-10: does not award badges for articles outside lookback window

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award badges for articles outside lookback window

### S-11: does not award badges to users who received it within the last week

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not award badges to users who received it within the last week

### S-12: allows awarding badge again after a week

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows awarding badge again after a week

