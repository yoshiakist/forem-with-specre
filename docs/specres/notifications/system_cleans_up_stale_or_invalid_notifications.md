---
id: "01KJ15Z6XANFFT1FA0YP2J2EQC"
name: "system_cleans_up_stale_or_invalid_notifications"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/notifications/remove_all.rb`
- `app/services/notifications/remove_all_by_action.rb`
- `app/services/notifications/remove_by_spammer.rb`
- `app/workers/notifications/remove_all_worker.rb`
- `app/workers/notifications/remove_by_spammer_worker.rb`
- `app/workers/notifications/remove_old_notifications_worker.rb`
- `spec/services/notifications/remove_all_spec.rb` (Test)
- `spec/services/notifications/remove_all_by_action_spec.rb` (Test)
- `spec/workers/notifications/remove_all_worker_spec.rb` (Test)
- `spec/workers/notifications/remove_by_spammer_worker_spec.rb` (Test)
- `spec/workers/notifications/remove_old_notifications_worker_spec.rb` (Test)

## Functional Overview

The system provides a set of background workers and service objects that remove notifications under three distinct circumstances: when all notifications tied to a specific set of notifiable records (articles, comments, or mentions) must be purged; when notifications for a set of notifiable records filtered by a specific action must be removed; and when a user is identified as a spammer and all notifications produced by their follows, comments, and published articles must be deleted. A fourth worker periodically purges aged notifications via a bulk fast-destroy path. All workers run on the low-priority Sidekiq queue and skip processing immediately if required inputs are absent or invalid.

## Design Intent

Each removal scenario is encapsulated in its own service class (`Notifications::RemoveAll`, `Notifications::RemoveAllByAction`, `Notifications::RemoveBySpammer`), keeping the logic thin and testable in isolation. Workers act purely as async shells that validate inputs and delegate to the service, preventing unnecessary database work when job arguments are stale or malformed. Using `delete_all` rather than `destroy_all` intentionally bypasses ActiveRecord callbacks for performance, appropriate for bulk cleanup operations.

## Scenarios

### Remove all notifications for a set of notifiable records

1. A caller enqueues `Notifications::RemoveAllWorker` with a list of notifiable IDs and a notifiable type string.
2. The worker validates that the type is one of `Article`, `Comment`, or `Mention`, and that the ID list is non-empty; if either check fails, it returns without acting.
3. The worker delegates to `Notifications::RemoveAll`, which deletes all notifications whose `notifiable_type` and `notifiable_id` match the provided values.

### Remove notifications for a set of notifiable records scoped by action

1. A caller invokes `Notifications::RemoveAllByAction` with a list of notifiable IDs, a notifiable type, and an action string.
2. The service validates the type against the allowed set (`Article`, `Comment`, `Mention`) and that IDs are present; otherwise it returns without acting.
3. The service resolves the notifiable records and deletes all notifications that match both the resolved collection and the given action (e.g., only "Published" notifications for a set of articles).

### Remove all notifications produced by a spammer

1. A caller enqueues `Notifications::RemoveBySpammerWorker` with the ID of a user flagged as a spammer.
2. The worker looks up the user; if the user does not exist, it returns without acting.
3. The worker delegates to `Notifications::RemoveBySpammer`, which deletes notifications tied to the user's follows, comments, and published articles in three separate targeted queries.

### Purge aged notifications on a schedule

1. A scheduler enqueues `Notifications::RemoveOldNotificationsWorker` periodically.
2. The worker calls `Notification.fast_destroy_old_notifications`, which bulk-deletes notifications that have exceeded the configured age threshold.

## Failures / Exceptions

- `Notifications::RemoveAllWorker` and `Notifications::RemoveAll` silently skip execution when the notifiable type is not one of `Article`, `Comment`, or `Mention`, or when the ID list is empty.
- `Notifications::RemoveBySpammerWorker` silently skips execution when the provided user ID does not resolve to an existing user record.
- `Notifications::RemoveAllByAction` applies the same type/ID guard as `RemoveAll`; an unsupported type or empty ID list results in a no-op.
