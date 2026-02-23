---
id: "01KJ15ND4TPFS7E01YWS9GX3EC"
name: "system_notifies_user_on_new_comment"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/notifications/new_comment/send.rb`
- `app/workers/comments/send_email_notification_worker.rb`
- `app/views/notifications/_comment.html.erb` (Template)
- `app/sanitizers/comment_email_scrubber.rb`
- `spec/services/notifications/new_comment/send_spec.rb` (Test)
- `spec/workers/comments/send_email_notification_worker_spec.rb` (Test)

## Functional Overview

When a new comment is created, `Notifications::NewComment::Send` determines which users should receive an in-app notification and dispatches mobile push notifications to eligible users. It builds a deduplicated set of recipient user IDs from four sources: authors of ancestor comments who have notifications enabled, users subscribed to all comments on the article, users subscribed to top-level comments only (skipped for replies), and users subscribed to author-only comments (applied only when the commenter is also the article author). The comment's own author is excluded from the recipient set. Comments with a negative score are silently skipped. A separate Sidekiq worker, `Comments::SendEmailNotificationWorker`, handles email delivery by invoking `NotifyMailer` for the same comment, again skipping comments with a negative score. The notification template (`_comment.html.erb`) renders the in-app notification card, differentiating between plain comments, moderation events, and first-comment events.

## Design Intent

Recipient resolution is composed from four independent subscription queries merged into a `Set`, ensuring deduplication without database-level `DISTINCT`. The commenter is removed from the set afterward rather than at query time, keeping each query simple. Mobile push notifications re-query the database with a join against `notification_setting` so that only users who opted in to mobile comment notifications receive pushes, decoupling delivery-channel preferences from subscription-topic preferences. Email delivery is intentionally offloaded to a dedicated Sidekiq worker on the `mailers` queue rather than performed synchronously, allowing the main notification fan-out to complete without blocking on mail delivery.

## Key Members

- `comment.score` — if negative, all notification delivery is skipped entirely
- `comment.ancestry` — presence indicates the comment is a reply; used to exclude top-level-only subscribers
- `comment.user_id` vs `comment.commentable.user_id` — equality check determines whether author-subscriber notifications apply
- `NotificationSubscription#config` — enum-like string (`"all_comments"`, `"top_level_comments"`, `"only_author_comments"`) controlling which subscription bucket a user belongs to

## Scenarios

### Notification fan-out for a new comment

1. A new comment is posted on an article.
2. The system calls `Notifications::NewComment::Send` with the comment.
3. If the comment's score is negative, the system returns immediately and no notifications are sent.
4. Otherwise, the system collects recipient IDs from: ancestor comment authors with notifications enabled, users subscribed to all comments, top-level subscribers (if the comment has no parent), and author-subscribers (if the commenter is also the article author).
5. The comment's own author is removed from the recipient set.
6. An in-app `Notification` record is created for each remaining recipient, carrying the commenter's user data and comment data as JSON.

### Mobile push notification delivery

1. After in-app notifications are created, the system queries the recipient set for users who have `mobile_comment_notifications` enabled in their notification settings.
2. `PushNotifications::Send` is called with those user IDs, a title, a body composed from the commenter's username and the article title, and a payload containing the comment URL and type `"new comment"`.

### Organization notification

1. After user notifications are dispatched, if the article's commentable belongs to an organization (i.e., `organization_id` is present), an additional `Notification` record is created scoped to that organization.
2. No push notification is sent for organizations.

### Email notification via background worker

1. `Comments::SendEmailNotificationWorker` is enqueued with the comment ID on the `mailers` queue.
2. When performed, the worker looks up the comment by ID.
3. If the comment does not exist or has a negative score, no email is sent.
4. Otherwise, `NotifyMailer` delivers a `new_reply_email` synchronously within the worker.

### Top-level subscriber exclusion for replies

1. A user is subscribed to `top_level_comments` on an article.
2. A reply comment (one with an ancestor) is posted.
3. The system detects that the comment has ancestry and skips the top-level subscription bucket entirely.
4. The subscriber does not receive a notification for the reply.

## Failures / Exceptions

- If the comment's score is already negative at call time, `Notifications::NewComment::Send#call` returns immediately without creating any `Notification` records or dispatching push notifications.
- If the comment cannot be found by ID in `Comments::SendEmailNotificationWorker#perform`, the worker exits without raising an error and no email is sent.
- If the comment is found but its score is not greater than `-1`, the worker skips email delivery without raising an error.
