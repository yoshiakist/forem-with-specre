---
id: "01KJ162B266JS6N6VM0EMQWB02"
name: "system_delivers_push_notifications"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/push_notifications/send.rb`
- `app/workers/push_notifications/deliver_worker.rb`
- `app/workers/push_notifications/cleanup_worker.rb`
- `spec/services/push_notifications/send_spec.rb` (Test)

## Functional Overview

When the system needs to send push notifications to one or more users, `PushNotifications::Send` looks up every registered device belonging to those users and creates a pending notification on each device via the Rpush library. Once the notifications are staged, it schedules `PushNotifications::DeliverWorker` to run 30 seconds later, which calls `Rpush.push` to flush all pending notifications in a single batch. The 30-second delay and a Sidekiq uniqueness lock (`until_expired`, TTL 30 s) ensure that many rapid calls to `Send` collapse into at most one delivery job per window, avoiding redundant processing. A separate `PushNotifications::CleanupWorker` runs on a low-priority queue and scans Redis for delivered Rpush notification records that have no expiry set, applying an 8-hour TTL to prevent unbounded Redis growth.

## Design Intent

The batching pattern — staging notifications immediately and scheduling a single deferred delivery job — is an explicit cost-control decision documented in the source: even if `Send` is called once every 5 seconds, only one `DeliverWorker` executes per 30-second window. The `on_conflict: :log` option on `DeliverWorker` means duplicate scheduling attempts are silently discarded after logging, keeping the queue clean. `CleanupWorker` exists because Rpush does not automatically expire delivered notification records in Redis, so without it the keyspace would grow indefinitely.

## Scenarios

### No registered devices for target users

1. Caller invokes `PushNotifications::Send` with one or more user IDs.
2. The service queries `Device` for records matching those user IDs and finds none.
3. No Rpush notifications are created and `PushNotifications::DeliverWorker` is not enqueued.

### Single device — notification staged and delivery scheduled

1. Caller invokes `PushNotifications::Send` with a user ID, title, body, and payload.
2. The service finds one device for that user and calls `create_notification` on it, which persists a pending Rpush notification record.
3. Because at least one device was found, `PushNotifications::DeliverWorker` is scheduled to run 30 seconds from now.
4. When `DeliverWorker` performs, it calls `Rpush.push` to dispatch all pending notifications and then `Rpush.apns_feedback` to process APNs delivery receipts.

### Multiple devices across multiple users

1. Caller invokes `PushNotifications::Send` with several user IDs.
2. The service iterates over every registered device across all target users and stages one Rpush notification per device.
3. Exactly one `PushNotifications::DeliverWorker` job is enqueued regardless of how many devices were found, because the uniqueness lock discards duplicates.

### Non-operational consumer app suppresses notification creation

1. A device is registered under a `ConsumerApp` that lacks a valid `auth_key` (non-operational).
2. The service iterates the device and calls `create_notification`, but the `ConsumerApp` guard inside that method prevents a Rpush notification record from being saved.
3. No Rpush notifications are persisted for that device.

### Cleanup of delivered Redis keys

1. `PushNotifications::CleanupWorker` is invoked on the low-priority Sidekiq queue.
2. It opens a Redis connection using `REDIS_RPUSH_URL` (falling back to `REDIS_URL`) and scans all keys matching `rpush:notifications:*`.
3. For each key that is a hash, has a `delivered` field set, and has no existing TTL, it applies an 8-hour expiry.
4. Keys that are not hashes, lack a `delivered` field, or already have a TTL are skipped.

## Failures / Exceptions

- `PushNotifications::DeliverWorker` is configured with `retry: 10`, so transient failures during `Rpush.push` are retried up to 10 times before the job is dead-lettered.
- If `DeliverWorker` is enqueued while an identical job is still within its 30-second lock window, Sidekiq logs the conflict (`on_conflict: :log`) and discards the duplicate without raising an error.
- `CleanupWorker` uses `lock: :until_and_while_executing` to prevent concurrent cleanup runs; overlapping invocations are held until the current run completes.
