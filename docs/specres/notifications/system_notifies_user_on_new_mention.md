---
id: "01KJ15RRNWK6ZYZCX7KQF726AT"
name: "system_notifies_user_on_new_mention"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/notifications/new_mention/send.rb`
- `app/workers/notifications/mention_worker.rb`
- `app/workers/mentions/send_email_notification_worker.rb`
- `app/views/notifications/_mention.html.erb` (Template)
- `spec/services/notifications/new_mention/send_spec.rb` (Test)
- `spec/workers/notifications/mention_worker_spec.rb` (Test)
- `spec/workers/mentions/send_email_notification_worker_spec.rb` (Test)

## Functional Overview

When a user is mentioned in an article or comment, the system dispatches two asynchronous Sidekiq jobs: one to create an in-app `Notification` record and optionally send a mobile push notification, and another to deliver a mention email via `NotifyMailer`. The in-app notification is skipped entirely if the mentionable content has a negative score. Mobile push notifications are only sent when the mentioned user has enabled `mobile_mention_notifications` in their notification settings. The notification payload stores structured JSON data about the mentioner and the mentionable context (article or comment), which is used to render the mention notification card in the UI.

## Design Intent

The behavior is split into two independent Sidekiq workers — one for in-app and push notifications (`Notifications::MentionWorker`) and one for email (`Mentions::SendEmailNotificationWorker`) — so that email delivery failures do not block in-app notification creation, and each path can be retried and queued independently. The email worker runs on the `default` queue while the in-app worker runs on `low_priority`, reflecting the relative urgency of each channel.

## Key Members

- `mention.mentionable` — the content object (Article or Comment) in which the mention appears; its `score` controls whether the notification is suppressed
- `Users::NotificationSetting#mobile_mention_notifications?` — user preference gate for mobile push notifications
- `json_data` — serialized hash stored on the `Notification` record; contains `user` and either `article` or `comment` sub-keys used by the template

## Scenarios

### In-app notification created for a mention in an article

1. A `Mention` record is created linking a user to an article.
2. `Notifications::MentionWorker` is enqueued with the mention ID.
3. The worker looks up the `Mention` by ID and delegates to `Notifications::NewMention::Send`.
4. The service checks that the article's score is not negative; if it is, processing stops with no notification created.
5. A `Notification` record is created for the mentioned user, typed as `notifiable_type: "Mention"`, with `json_data` containing the mentioner's user data and the article's data.

### In-app notification created for a mention in a comment

1. A `Mention` record is created linking a user to a comment.
2. `Notifications::MentionWorker` is enqueued and the service is invoked.
3. The service creates a `Notification` record; `json_data` contains the mentioner's user data and the comment's data.

### Mobile push notification sent when user has opted in

1. After the in-app notification is persisted, the service checks `Users::NotificationSetting` for `mobile_mention_notifications?`.
2. If enabled, `PushNotifications::Send` is called with the mentioned user's ID, a localized title, and a body that includes the mentioner's username and a stripped excerpt of the mentionable content.
3. The push payload includes the URL to the mentionable and a `type` of `"new mention"`.

### Mobile push notification suppressed when user has opted out

1. The in-app `Notification` record is created as normal.
2. The service finds that `mobile_mention_notifications?` is false for the mentioned user.
3. `PushNotifications::Send` is not called; only the in-app record is written.

### Mention email delivered via NotifyMailer

1. `Mentions::SendEmailNotificationWorker` is enqueued with the mention ID.
2. The worker looks up the `Mention` by ID; if not found, it returns without error.
3. If found, it calls `NotifyMailer.with(mention: mention).new_mention_email.deliver_now` to send the email immediately.

## Failures / Exceptions

- If the mention record cannot be found by ID (e.g., it was deleted before the job ran), `Notifications::MentionWorker` skips processing silently and `Mentions::SendEmailNotificationWorker` returns early without raising an error.
- If the mentionable content has a negative score, `Notifications::NewMention::Send` returns immediately without creating any notification or sending a push notification.
