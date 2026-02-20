---
id: "01KHY7Q1K31WCEN3RP9XC7CM9R"
name: "ab_experiment_goal_conversion_handler_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/ab_experiment/goal_conversion_handler.rb
- app/models/ab_experiment.rb
- spec/models/ab_experiment/goal_conversion_handler_spec.rb

## Functional Overview

This specification defines the expected behavior of `AbExperiment::GoalConversionHandler` within the ab_testing domain.

### Behavioral Areas

- **.call**: Ensures correct behavior under the specified conditions
- **with no experiments**: records a conversion when they post 4 within a week
- **with experiment that started to soon for some results**: registers some events but not others
- **with user who is part of field test and user_publishes_post goal**: gracefully handles a case where there are no tests
- **with user who is part of field test and user_creates_comment goal**: gracefully handles a case where there are no tests
- **with user who is part of field test and user_creates_pageview goal**: gracefully handles a case where there are no tests
- **with user who is part of field test and user_creates_article_reaction goal**: gracefully handles a case where there are no tests
- **with user who is not part of field test**: gracefully handles a case where there are no tests

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/ab_experiment/goal_conversion_handler.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/ab_experiment.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: gracefully handles a case where there are no tests

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** gracefully handles a case where there are no tests

### S-2: registers some events but not others

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** registers some events but not others

### S-3: records a conversion

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** records a conversion

### S-4: records weekly post publishing conversions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** records weekly post publishing conversions

### S-5: records a conversion when they post 4 within a week

- **Given** the system is in a standard operational state
- **When** they post 4 within a week
- **Then** records a conversion

### S-6: records a conversion

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** records a conversion

### S-7: records user_creates_comment_on_at_least_four_different_days_within_a_week field...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** records user_creates_comment_on_at_least_four_different_days_within_a_week field test conversion

### S-8: records a field test when user views a page

- **Given** the system is in a standard operational state
- **When** user views a page
- **Then** records a field test

### S-9: records user_views_pages_on_at_least_two_different_days_within_a_week field test...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** records user_views_pages_on_at_least_two_different_days_within_a_week field test conversion

### S-10: records user_views_pages_on_at_least_four_different_days_within_a_week field tes...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** records user_views_pages_on_at_least_four_different_days_within_a_week field test conversion

### S-11: records user_views_pages_on_at_least_nine_different_days_within_two_weeks field ...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** records user_views_pages_on_at_least_nine_different_days_within_two_weeks field test conversionn

### S-12: records user_views_pages_on_at_least_twelve_different_hours_within_five_days fie...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** records user_views_pages_on_at_least_twelve_different_hours_within_five_days field test conversion

