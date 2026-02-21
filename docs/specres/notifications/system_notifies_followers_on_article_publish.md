---
id: "01KJ15YY7SWMF93P655KXRSPEK"
name: "system_notifies_followers_on_article_publish"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/notifications/notifiable_action/send.rb`
- `app/workers/notifications/notifiable_action_worker.rb`
- `app/models/context_notification.rb`
- `app/views/notifications/_article.html.erb` (Template)
- `spec/services/notifications/notifiable_action/send_spec.rb` (Test)
- `spec/workers/notifications/notifiable_action_worker_spec.rb` (Test)
- `spec/models/context_notification_spec.rb` (Test)
- `spec/factories/context_notifications.rb` (Test)

## Functional Overview

When an article is published, the system enqueues a `Notifications::NotifiableActionWorker` Sidekiq job that delegates to `Notifications::NotifiableAction::Send`. The service collects all users who follow either the article author or the author's organization with a subscription status of `all_articles`, excluding the article author themselves and any followers who were already mentioned in the article. For each qualifying follower it builds a notification record containing serialized user, article, and optional organization data. If any notifications are produced, the service upserts all `Notification` rows and a single `ContextNotification` row inside one database transaction, ensuring idempotent delivery even if the job runs more than once.

## Design Intent

`ContextNotification` exists specifically to record which publish events have already triggered follower notifications, guarding against duplicate fan-out. The upsert strategy (choosing the appropriate unique index based on whether `action` is present) makes the entire operation safe to retry without creating duplicate notification records.

## Key Members

- `FOLLOWER_SEND_LIMIT` — caps the follower query at 10,000 recently-active users to prevent unbounded fan-out on large accounts.
- `action` — currently only `"Published"` is supported; the parameter leaves room for future action types.
- `ContextNotification` — validated to accept only `action: "Published"` and `context_type: "Article"`, enforcing the current scope of this behavior.

## Scenarios

### Follower of author receives a notification

1. A follower has followed the article's author with subscription status `all_articles`.
2. `Notifications::NotifiableActionWorker` is performed with the article ID, type `"Article"`, and action `"Published"`.
3. The worker looks up the article and calls `Notifications::NotifiableAction::Send`.
4. The service finds the follower via an inner join on the follows table, filtered by subscription status.
5. A `Notification` record is upserted for the follower containing serialized article and author data, and a `ContextNotification` record is upserted for the article.

### Follower of organization receives a notification

1. A follower has followed the article author's organization with subscription status `all_articles`.
2. The service includes both user-follows and organization-follows in the same query.
3. A `Notification` record is upserted for the organization follower; its `json_data` includes both author and organization fields.
4. The same `ContextNotification` record is written for the article.

### Mentioned follower is excluded from follower notifications

1. A user follows the article's author but is also mentioned in the article body.
2. The service collects user IDs that have a `Mention` record linked to the article.
3. That user is excluded from the follower query, so no duplicate notification is created on top of the mention notification.

### Follower with muted subscription receives no notification

1. A follower's follow record has `subscription_status` set to a value other than `all_articles` (e.g., `"none"`).
2. The service's query filters only for `all_articles` subscriptions, so the follower is excluded.
3. No `Notification` or `ContextNotification` records are created.

### Article author following their own organization is not self-notified

1. The article author also follows the organization under which the article is published.
2. The service explicitly excludes the article's author from the follower query.
3. No notification is created for the author.

## Failures / Exceptions

- If the notifiable is not an `Article`, `Notifications::NotifiableAction::Send#call` returns immediately without creating any records.
- If the worker receives a `notifiable_type` other than `"Article"`, it returns before loading the record or calling the service.
- If the article no longer exists by the time the worker runs, the service is not called and no records are created.
- If `notifications_attributes` is empty after filtering (e.g., all followers are mentioned or muted), the method returns early and neither `Notification` nor `ContextNotification` records are written.
- Duplicate job execution is handled safely: both `Notification.upsert_all` and `ContextNotification.upsert` are idempotent, so re-running the job does not create duplicate records.
