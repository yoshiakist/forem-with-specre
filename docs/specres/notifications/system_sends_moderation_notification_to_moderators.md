---
id: "01KJ15W12WTJVFF3XQ1NJH5BNQ"
name: "system_sends_moderation_notification_to_moderators"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/notifications/moderation/send.rb`
- `app/workers/notifications/create_round_robin_moderation_notifications_worker.rb`
- `spec/services/notifications/moderation/send_spec.rb` (Test)
- `spec/workers/notifications/create_round_robin_moderation_notifications_worker_spec.rb` (Test)

## Functional Overview

When a comment or article is flagged for moderation, the system selects up to four available moderators at random via a round-robin mechanism and sends each of them a moderation notification. The worker (`CreateRoundRobinModerationNotificationsWorker`) queries eligible moderators, resolves the notifiable record, and then delegates notification creation to `Notifications::Moderation::Send`. The send service builds a `Notification` record with action `"Moderation"`, embedding staff-account user data and content-owner user data in a JSON payload, and updates the moderator's `last_moderation_notification` timestamp. Notifications are skipped entirely when no moderators are available, the notifiable record is missing, the content author has the `limited` role, or the moderator is the same user as the content author.

## Design Intent

The round-robin approach caps notification fan-out at `MODERATOR_SAMPLE_SIZE` (4) randomly ordered moderators per event, preventing notification fatigue while ensuring fresh moderators are rotated in. The `last_moderation_notification` timestamp is updated after each delivery so that `Users::SelectModeratorsQuery` can use availability windows to exclude recently-notified moderators from future rounds.

## Key Members

- `MODERATOR_SAMPLE_SIZE` — maximum number of moderators notified per round-robin invocation (value: 4)
- `SUPPORTED` — the set of notifiable types that trigger a notification: `Comment` and `Article`
- `MODERATORS_AVAILABILITY_DELAY` — cooldown window (22 hours) used by the moderator selection query to determine availability

## Scenarios

### Notification sent for a comment

1. The worker receives a `notifiable_id` and `notifiable_type` of `"Comment"`.
2. It queries for available moderators in random order and takes the first four.
3. It looks up the `Comment` record by ID and verifies that its commentable still exists.
4. It confirms the comment author is not limited.
5. For each moderator who is not the comment's author, `Notifications::Moderation::Send` is called.
6. The service creates a `Notification` with action `"Moderation"`, associating it with the moderator and embedding staff-account and comment-author data in `json_data`.
7. The moderator's `last_moderation_notification` is updated to the current time.

### Notification sent for an article

1. The worker receives a `notifiable_id` and `notifiable_type` of `"Article"`.
2. It queries for available moderators in random order and takes the first four.
3. It looks up the `Article` record by ID.
4. It confirms the article author is not limited.
5. For each moderator who is not the article's author, `Notifications::Moderation::Send` is called.
6. The service creates a `Notification` with action `"Moderation"`, associating it with the moderator and embedding staff-account and article-author data in `json_data`.
7. The moderator's `last_moderation_notification` is updated to the current time.

### Notification skipped — no available moderators

1. The worker queries for moderators but none meet the availability criteria.
2. The worker exits early without calling `Notifications::Moderation::Send`.

### Notification skipped — content author is limited or is the moderator

1. The worker resolves the notifiable record and selects random moderators.
2. When iterating moderators, any moderator who is the content author is skipped.
3. If the content author carries the `limited` role, the worker exits before the loop and no notification is sent.

### Notification skipped — notifiable record not found or commentable deleted

1. The worker attempts to find the notifiable record by ID.
2. If no record is found, or if the comment's commentable has been deleted, the worker exits early without calling `Notifications::Moderation::Send`.

## Failures / Exceptions

- If the notifiable type is not `Comment` or `Article`, the send service returns immediately because only those types are included in `SUPPORTED`.
- If the `Comment` record exists but its commentable has been destroyed, the worker aborts before dispatching any notifications.
- If no moderators are available (empty result from `Users::SelectModeratorsQuery`), no notifications are sent and no error is raised.
