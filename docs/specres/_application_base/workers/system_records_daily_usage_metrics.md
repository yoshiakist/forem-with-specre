---
id: "01KJVP58C9EFXMZQWJ0JYF7004"
name: "system_records_daily_usage_metrics"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/workers/metrics/record_daily_usage_worker.rb`
- `spec/workers/metrics/record_daily_usage_worker_spec.rb` (Test)

## Functional Overview

The `Metrics::RecordDailyUsageWorker` is a low-priority Sidekiq job that runs daily to collect and report a set of platform health and engagement metrics. It queries the database for counts of notable articles, engaged new users, negative reactions, and abuse reports from the past 24 hours, then sends each count to `ForemStatsClient` with descriptive metric keys and resource tags. It also analyzes a full week of `PageView` data to produce per-day-count distributions of active users, segmented into "established" and "new" user groups, giving the platform a picture of weekly engagement depth.

## Scenarios

### Record high-scoring article metrics for the past 24 hours

1. The worker queries for published articles from the current subforem whose `score` is 15 or above and whose `published_at` falls within the past 24 hours.
2. The resulting count is sent to `ForemStatsClient` under the metric key `articles.min_15_score_past_24h` with the tag `resource:articles`.
3. The worker similarly queries for articles whose `comment_score` is 15 or above and published within the past 24 hours.
4. That count is sent under the key `articles.min_15_comment_score_past_24h` with the same resource tag.

### Record first-article publications for the past 24 hours

1. The worker queries for articles where `nth_published_by_author` equals 1 (meaning it was that author's debut post) and `published_at` is within the past 24 hours.
2. The count is sent to `ForemStatsClient` under `articles.first_past_24h` with the tag `resource:articles`.

### Record new users with at least one comment

1. The worker queries for users who registered within the past 24 hours and have a `comments_count` of 1 or more.
2. The count is sent to `ForemStatsClient` under `users.new_min_1_comment_past_24h` with the tag `resource:users`.

### Record negative reactions and abuse reports

1. The worker counts all reactions with negative points created within the past 24 hours and sends the total under `reactions.negative_past_24h` with the tag `resource:reactions`.
2. It then counts `FeedbackMessage` records in the categories "spam", "other", "rude or vulgar", and "harassment" created within the past 24 hours, sending the total under `feedback_messages.reports_past_24_hours` with the tag `resource:feedback_messages`.

### Record weekly active-day distribution for users

1. The worker collects distinct user IDs from `PageView` for each of the past 7 days, building a list of unique visitors per day.
2. It separates the visitors into two groups: users registered more than 7 days ago ("established") and users who registered in the 7–8 day window ("new").
3. For each group, it counts how many users appeared on exactly 1 day, exactly 2 days, and so on, up to 7 days.
4. Each per-day-count bucket is sent to `ForemStatsClient` under `users.active_days_past_week` with tags for `resource:users`, the group name, and the day count.
