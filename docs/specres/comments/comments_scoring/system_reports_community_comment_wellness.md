---
id: "01KJ44GE4DQCP13GD0ENDND135"
name: "system_reports_community_comment_wellness"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/queries/comments/community_wellness_query.rb`
- `spec/queries/comments/community_wellness_query_spec.rb` (Test)

## Functional Overview

`Comments::CommunityWellnessQuery` runs a raw SQL query against the database and returns an array of hashes that summarize, per user, how many non-negatively-reacted comments they posted in each calendar week over the past 231 days. Each hash contains a `user_id`, a comma-separated string of `serialized_weeks_ago` values (e.g. `"0,1,2"`), and a corresponding comma-separated string of `serialized_comment_counts`. Only users who posted more than one comment during the most recent completed week (7–14 days ago) are included in the result set, making the output the raw ingredient for evaluating eligibility for the Community Wellness Badge.

## Design Intent

The query intentionally uses `ActiveRecord::Base.connection.execute` and returns plain hashes rather than ActiveRecord objects, because the result set does not map to any single model and materializing AR objects would add overhead with no benefit. The 231-day (33-week) window balances historical depth against query performance, and the minimum-two-comments-in-week-1 filter is applied as an early join condition to eliminate low-activity users before the per-week aggregation.

## Key Members

- `serialized_weeks_ago` — comma-separated integers representing how many full weeks ago (from now) each group of comments was posted, ordered by aggregation
- `serialized_comment_counts` — comma-separated integers representing the count of positively-reacted comments for each corresponding week in `serialized_weeks_ago`
- Negative reaction categories filtered out: `thumbsdown`, `vomit`
- Lookback window: 231 days (33 weeks)
- Minimum activity filter: user must have more than 1 comment in the week that is 7–14 days ago

## Scenarios

### Returns structured data for qualifying users

1. The caller invokes `Comments::CommunityWellnessQuery.call`.
2. The system queries all comments created within the past 231 days that have not received a `thumbsdown` or `vomit` reaction.
3. For each such comment the system calculates how many full weeks ago it was created relative to the current timestamp.
4. The system groups the comments by user and week, counting comments per week.
5. Only users who posted more than one comment during the most recent completed week (7–14 days ago) are retained.
6. The system returns an array of hashes, one per qualifying user, each with integer `user_id`, string `serialized_weeks_ago`, and string `serialized_comment_counts`.

### Excludes users with fewer than two comments in the anchor week

1. A user has posted only one comment in the 7–14 day window.
2. When `Comments::CommunityWellnessQuery.call` runs, that user does not satisfy the minimum-activity join condition.
3. The user is absent from the returned array.

### Excludes comments that are too old

1. A user has multiple comments but all of them were created more than 231 days ago.
2. The query's date filter (`created_at > now() - interval '231' day`) excludes those comments from every subquery.
3. The user does not appear in the result set regardless of their historical comment volume.

### Reduces per-week counts when a moderator flags a comment

1. A user has two comments in a given week, but one of those comments carries a `thumbsdown` or `vomit` reaction.
2. The query's `EXCEPT` clause removes the flagged comment's ID from the eligible set before aggregation.
3. The week's count for that user is decremented by the number of negatively-reacted comments, and the reduced count appears in `serialized_comment_counts` for that week's position.

### Returns empty array when no users meet the criteria

1. No users have posted more than one comment in the 7–14 day anchor window.
2. The minimum-activity join eliminates all candidates.
3. `Comments::CommunityWellnessQuery.call` returns an empty array.

## Failures / Exceptions

- No explicit error handling is present in the query class; any database error raised by `ActiveRecord::Base.connection.execute` will propagate to the caller unchanged.
