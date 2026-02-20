---
id: "01KHY7Q0Z8X1AP0QCX4Y749B83"
name: "analytics_service_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/analytics_service.rb
- app/services/articles/page_view_updater.rb
- app/services/page_view_rollup.rb
- spec/services/analytics_service_spec.rb

## Functional Overview

This specification defines the expected behavior of `AnalyticsService` within the analytics domain.

### Behavioral Areas

- **initialization**: Ensures correct behavior under the specified conditions
- **totals**: returns totals stats for comments, reactions, follows and page views
- **comments stats**: returns totals stats for comments, reactions, follows and page views
- **reactions stats**: returns totals stats for comments, reactions, follows and page views
- **follows stats**: returns totals stats for comments, reactions, follows and page views
- **page views stats**: returns totals stats for comments, reactions, follows and page views
- **grouped_by_day**: Ensures correct behavior under the specified conditions
- **comments stats on a specific day**: returns totals stats for comments, reactions, follows and page views

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/analytics_service.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/page_view_updater.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/page_view_rollup.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: raises an error if start date is invalid

- **Given** start date is invalid
- **When** the action is triggered
- **Then** raises an error

### S-2: raises an error if end date is invalid

- **Given** end date is invalid
- **When** the action is triggered
- **Then** raises an error

### S-3: raises an error if an article does not belong to the user

- **Given** an article does not belong to the user
- **When** the action is triggered
- **Then** raises an error

### S-4: returns totals stats for comments, reactions, follows and page views

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns totals stats for comments, reactions, follows and page views

### S-5: returns totals stats for an org

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns totals stats for an org

### S-6: returns stats

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns stats

### S-7: returns the total number of comments

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the total number of comments

### S-8: returns zero as total if there are no scored comments

- **Given** there are no scored comments
- **When** the action is triggered
- **Then** returns zero as total

### S-9: returns stats

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns stats

### S-10: returns the total number of reactions

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the total number of reactions

### S-11: returns zero as total if there are no public category reactions

- **Given** there are no public category reactions
- **When** the action is triggered
- **Then** returns zero as total

### S-12: returns the number of like reactions

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the number of like reactions

