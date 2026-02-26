---
id: "01KJBWVJKSF1WMNK6YAXZKQK08"
name: "system_notifies_on_article_publish"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/workers/articles/publish_worker.rb`
- `app/services/slack/messengers/article_published.rb`
- `spec/workers/articles/publish_worker_spec.rb` (Test)
- `spec/services/slack/messengers/article_published_spec.rb` (Test)

## Functional Overview

When articles are published, a background worker periodically finds recently published articles that have not yet had context notifications created, and for each one: sends a Slack message announcing the publication, dispatches in-app notifications to any users mentioned in the article, and notifies users who follow the article's author. The Slack messenger guards against sending duplicate or stale notifications by skipping articles published more than 10 minutes ago and skipping altogether when the `DISABLE_SLACK_NOTIFICATIONS` environment variable is set to `"true"`.

## Design Intent

The worker uses a 30-minute look-back window combined with the absence of a `context_notifications_published` association to identify articles that need processing. This idempotency check prevents double-notifying if the worker runs more than once within its window.

## Scenarios

### Worker dispatches notifications for a newly published article

1. The worker queries for articles that are marked published, whose `published_at` falls within the past 30 minutes, and that lack an associated context notification record.
2. For each matching article, the worker calls `Slack::Messengers::ArticlePublished` to send a Slack announcement.
3. The worker calls `Notification.send_to_mentioned_users_and_followers` for the article, which enqueues `Notifications::NotifiableActionWorker` to create in-app notifications for mentioned users and followers of the author.

### Slack messenger sends a message for a recently published article

1. `Slack::Messengers::ArticlePublished` is called with an article that is published and whose `published_at` is within the past 10 minutes.
2. The messenger composes a message containing the article title and its public URL.
3. The messenger enqueues `Slack::Messengers::Worker` targeting the configured `article_published_slack_channel`, with username `article_bot` and the `:writing_hand:` emoji.

### Worker skips articles outside the time window

1. An article was published more than 30 minutes ago (or is scheduled with a future `published_at`).
2. The worker's query does not include the article.
3. No Slack message and no in-app notifications are sent for that article.

### Slack messenger skips stale or draft articles

1. `Slack::Messengers::ArticlePublished` is called with an article that is either a draft (`published: false`) or was published more than 10 minutes ago.
2. The messenger returns early without enqueuing any Slack job.

## Failures / Exceptions

- If `DISABLE_SLACK_NOTIFICATIONS` is set to `"true"`, the Slack messenger returns immediately without sending any message, regardless of article state.
