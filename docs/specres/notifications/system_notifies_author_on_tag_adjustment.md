---
id: "01KJ15W5XTEVQVJN1FCRNWEKAB"
name: "system_notifies_author_on_tag_adjustment"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/notifications/tag_adjustment_notification/send.rb`
- `app/workers/notifications/tag_adjustment_notification_worker.rb`
- `app/views/notifications/_tagadjustment.html.erb` (Template)
- `spec/services/notifications/tag_adjustment_notification/send_spec.rb` (Test)
- `spec/workers/notifications/tag_adjustment_notification_worker_spec.rb` (Test)

## Functional Overview

When a tag moderator adds or removes a tag from an article, the system enqueues a background job that creates an in-app notification for the article's author. The job looks up the `TagAdjustment` record by ID and delegates to `Notifications::TagAdjustmentNotification::Send`, which assembles a JSON payload containing the mascot account's user data, the article title and path, the adjustment type (`addition` or `removal`), the adjustment status, the reason for the adjustment, and the tag name. A `Notification` record is then persisted and attributed to the article author. The notification is rendered from the JSON payload, showing a localized message that differentiates between tag additions and removals and optionally displays the moderator's stated reason.

## Scenarios

### Tag added to an article

1. A tag moderator adds a tag to an article, producing a `TagAdjustment` record with `adjustment_type` set to `"addition"`.
2. `Notifications::TagAdjustmentNotificationWorker` is enqueued with the `TagAdjustment` ID on the `medium_priority` queue.
3. The worker looks up the `TagAdjustment` by ID; finding it, it calls `Notifications::TagAdjustmentNotification::Send`.
4. The service builds a JSON payload using the mascot account as the acting user and stores the article title, path, adjustment type, status, reason, and tag name.
5. A `Notification` record is created for the article author, associated with the `TagAdjustment` as the notifiable object.
6. The author sees an in-app notification indicating that the tag was added to their article.

### Tag removed from an article

1. A tag moderator removes a tag from an article, producing a `TagAdjustment` record with `adjustment_type` set to `"removal"`.
2. The same worker and service pipeline runs as for an addition.
3. The resulting notification presents a removal-specific message and includes a link to the tags page so the author can discover other relevant tags.

### Adjustment includes a reason

1. The moderator provides a `reason_for_adjustment` when creating the `TagAdjustment`.
2. The reason is included in the JSON payload stored on the `Notification`.
3. The notification view renders the reason inside a secondary card, making the moderation rationale visible to the author.

### Tag adjustment record not found

1. The worker receives a `tag_adjustment_id` that no longer corresponds to an existing `TagAdjustment` record (e.g., the record was deleted before the job ran).
2. The worker returns early without calling the send service, so no notification is created.

## Failures / Exceptions

- If the `TagAdjustment` record cannot be found by the given ID, the worker exits silently with no notification sent and no error raised.
- The worker is configured with up to 10 retries, so transient failures (e.g., database unavailability) are retried automatically before the job is discarded.
