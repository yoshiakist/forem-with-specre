---
id: "01KJ15RMG4PP6RC3KZN6JDG99C"
name: "system_notifies_user_on_new_follower"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/notifications/new_follower/send.rb`
- `app/services/notifications/new_follower/follow_data.rb`
- `app/workers/notifications/new_follower_worker.rb`
- `app/workers/follows/send_email_notification_worker.rb`
- `app/views/notifications/_follow.html.erb` (Template)
- `app/views/mailers/notify_mailer/new_follower_email.html.erb` (Template)
- `app/views/mailers/notify_mailer/new_follower_email.text.erb` (Template)
- `spec/services/notifications/new_follower/send_spec.rb` (Test)
- `spec/services/notifications/new_follower/follow_data_spec.rb` (Test)
- `spec/workers/notifications/new_follower_worker_spec.rb` (Test)
- `spec/workers/follows/send_email_notification_worker_spec.rb` (Test)

## Functional Overview

When a user or organization receives a new follower, the system creates or updates an aggregated in-app notification that groups all non-suspended followers from the past 24 hours. The `Notifications::NewFollower::Send` service accepts follow data (validated and coerced by `Notifications::NewFollower::FollowData`), queries recent non-suspended follows, and either upserts or destroys the notification record depending on whether any qualifying followers remain. The `Notifications::NewFollowerWorker` dispatches this service asynchronously on the `medium_priority` queue. Separately, `Follows::SendEmailNotificationWorker` delivers a `new_follower_email` via `NotifyMailer` when the followable user has email follower notifications enabled and a duplicate email has not already been sent within the recent deduplication window.

## Design Intent

- Follow data is passed between systems as a serializable hash, with `Notifications::NewFollower::FollowData` acting as a validated value object that can be coerced from a `Follow` record, an existing `FollowData` instance, or a plain hash. This guards against invalid data crossing async boundaries.
- The notification is aggregated over a 24-hour rolling window of recent follows so that a user receiving many followers in quick succession sees a single grouped notification rather than many individual ones. Suspended users are excluded from the aggregated siblings list.
- The email deduplication check uses a randomized window (15–35 hours) to spread load and prevent duplicate emails when multiple follow events occur close together.

## Key Members

- `followable_id` / `followable_type` — identify the entity being followed; `followable_type` must be `"User"` or `"Organization"`.
- `follower_id` — the integer ID of the following user.
- `is_read` — when `true`, the created notification is marked as already read (used for back-fill scenarios).
- `aggregated_siblings` — array of user data hashes for all non-suspended followers of the target within the past 24 hours, embedded in the notification's `json_data`.

## Scenarios

### Single user follows another user

1. A follow event is triggered; `Notifications::NewFollowerWorker` receives serialized follow data and enqueues a job on the `medium_priority` queue.
2. The worker calls `Notifications::NewFollower::Send` with the follow data.
3. `FollowData.coerce` validates the input and produces a typed value object; invalid types (e.g., tag follows) raise `Notifications::NewFollower::FollowData::DataError`.
4. The service queries all non-suspended follows targeting the same followable in the past 24 hours and builds an `aggregated_siblings` list.
5. A `Notification` record with `action: "Follow"` is created (or updated if one already exists), referencing the triggering follow as the notifiable and storing all siblings in `json_data`.

### Multiple users follow the same target within 24 hours

1. Each follow event triggers a separate `Notifications::NewFollowerWorker` job.
2. On each call, the service refreshes the aggregated siblings list to include all qualifying recent followers.
3. If a notification record already exists for the target with `action: "Follow"`, it is updated in place rather than creating a duplicate.
4. The notification's `notifiable` is set to the most recent triggering follow within the aggregated set.
5. Suspended users are excluded from the siblings list regardless of when they followed.

### User unfollows, removing the only recent follower

1. A stop-following event occurs; `Notifications::NewFollower::Send` is called with the unfollow data.
2. The service queries recent non-suspended follows and finds no qualifying followers remaining.
3. The existing `Notification` record for the target is destroyed.

### User unfollows when other recent followers still exist

1. A stop-following event occurs; `Notifications::NewFollower::Send` is called.
2. Remaining non-suspended followers still exist within the 24-hour window.
3. The notification is updated to reflect the current aggregated siblings; no notification is destroyed.

### System sends a new-follower email notification

1. When a follow is created, `Follows::SendEmailNotificationWorker` is enqueued on the `mailers` queue with the follow ID.
2. The worker looks up the follow; if the followable is absent or does not have follower email notifications enabled, the job exits without sending.
3. If a matching `EmailMessage` with the new-follower subject already exists within the deduplication window (15–35 hours), the job exits without sending.
4. Otherwise, `NotifyMailer` delivers `new_follower_email` immediately.

## Failures / Exceptions

- `Notifications::NewFollower::FollowData::DataError` is raised when the input follow data fails validation (e.g., `followable_type` is not `"User"` or `"Organization"`, or IDs are non-integer).
- If the follow record cannot be found (e.g., deleted before the worker runs), `Follows::SendEmailNotificationWorker` exits silently without error.
