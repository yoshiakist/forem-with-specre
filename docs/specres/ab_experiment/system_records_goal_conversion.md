---
id: "01KJ703F16P7AYF29Z4W9PQW5K"
name: "system_records_goal_conversion"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/models/ab_experiment.rb`
- `app/models/ab_experiment/goal_conversion_handler.rb`
- `app/workers/users/record_field_test_event_worker.rb`
- `spec/models/ab_experiment_spec.rb` (Test)
- `spec/models/ab_experiment/goal_conversion_handler_spec.rb` (Test)
- `spec/workers/users/record_field_test_event_worker_spec.rb` (Test)

## Functional Overview

Experiments and their goals are defined in `config/field_test.yml` and activated by deploying the configuration — there is no admin UI for experiment management. When a user performs an action, the system evaluates whether that action constitutes a goal conversion for any active experiments. `AbExperiment.register_conversions_for` delegates to `GoalConversionHandler`, which iterates over all configured experiments, skipping any that already have a declared winner. For each active experiment, the handler dispatches to goal-specific logic based on the goal name. Pageview, comment, post-publishing, and article reaction goals trigger cumulative threshold checks over various time windows (e.g., distinct days in the past week, distinct hours in the past day), recording separate named conversion events for each threshold met. Email feed event and other unrecognised goals fall back to a single direct conversion call. `Users::RecordFieldTestEventWorker` is a low-priority Sidekiq job that looks up a user by ID and delegates to `AbExperiment.register_conversions_for`, gracefully exiting if the user no longer exists.

## Design Intent

Conversion thresholds are deliberately cumulative: recording finer-grained engagement signals (e.g., "viewed pages on 4 different days in a week") alongside the base event allows experiments to measure depth of engagement, not just one-time actions. Experiments are scoped to their `started_at` date so that user activity predating the experiment does not pollute results. A feature flag gates the single-pageview base conversion to allow safe rollout without overheating the system with extra events.

## Key Members

- `USER_PUBLISHES_POST_GOAL` — goal name constant for post-publishing events
- `USER_CREATES_PAGEVIEW_GOAL` — goal name constant for page-view events
- `USER_CREATES_COMMENT_GOAL` — goal name constant for comment events
- `USER_CREATES_ARTICLE_REACTION_GOAL` — goal name constant for article reaction events
- `USER_CREATES_EMAIL_FEED_EVENT_GOAL` — goal name constant for email feed click events
- `started_at` — per-experiment date used to bound which historical activity qualifies

## Scenarios

### No active experiments

1. `register_conversions_for` is called with a nil or empty experiments hash.
2. The handler returns immediately without recording any conversion events.

### Experiment with a declared winner is skipped

1. An experiment in the configuration has a `winner` key set.
2. The handler iterates over experiments and skips that entry entirely, recording no events for it.

### User converts on a pageview goal with cumulative thresholds

1. A pageview event is triggered for a user enrolled in an active experiment.
2. The worker enqueues `Users::RecordFieldTestEventWorker` with the user ID and `user_creates_pageview` goal.
3. The handler optionally records the single-pageview base conversion if the `field_test_event_single_create_pageview` feature flag is enabled.
4. The handler queries the user's page views grouped by calendar day and by hour across several time windows (past week, past day, past two weeks, past five days).
5. For each window where the count of distinct days or hours meets or exceeds the threshold, a named conversion event is recorded (e.g., `user_views_pages_on_at_least_two_different_days_within_a_week`).
6. Activity that falls before the experiment's `started_at` date is excluded from the counts.

### User converts on a comment goal with threshold

1. A comment is created and `user_creates_comment` goal is fired for the user.
2. The handler records the base single-comment conversion.
3. If the user has commented on at least four distinct calendar days within the past week, an additional `user_creates_comment_on_at_least_four_different_days_within_a_week` conversion is recorded.

### User converts on a post-publishing goal with multiple thresholds

1. An article is published and `user_publishes_post` goal is fired.
2. The handler records the base single-post conversion.
3. If the user has published posts on at least four distinct calendar days within the past week, the `user_publishes_post_on_four_different_days_within_a_week` conversion is also recorded.
4. If the user has published at least two posts in the past week, `user_publishes_post_at_least_two_times_within_week` is recorded.
5. If the user has published at least two posts in the past two weeks, `user_publishes_post_at_least_two_times_within_two_weeks` is recorded.

### User converts on an article reaction goal

1. A reaction is created and `user_creates_article_reaction` goal is fired.
2. The handler records the base single-reaction conversion.
3. Only reactions to articles (`only_articles`) with a public category (`public_category`) are counted for the threshold check.
4. If the user has reacted on at least four distinct calendar days within the past week, `user_creates_article_reaction_on_four_different_days_within_a_week` is also recorded.

### User is not enrolled in the experiment

1. A goal event fires for a user who has never been assigned to any experiment variant.
2. The `field_test_converted` call finds no membership for the user and records no events.

### Worker receives a non-existent user ID

1. `Users::RecordFieldTestEventWorker` is invoked with a user ID that does not exist in the database.
2. The worker looks up the user with `find_by`, receives nil, and returns without calling `register_conversions_for`.

## Failures / Exceptions

- If `experiments` is nil, `GoalConversionHandler#call` returns early without error.
- If a user is deleted between the time the job is enqueued and when it runs, the worker exits gracefully without raising.
